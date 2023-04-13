#!/usr/bin/env python
# coding: utf-8

# In[26]:


import sys


class FakeRob:
    def __init__(self, instruction_list_string):
        self.ZERO_REPLACEMENT = 564654
        self.fake_rob_queue = []
        self.currIndex = 0
        data_string = instruction_list_string.split("\n")
        index = 1
        for instruction in data_string:
            temp_ins_list = instruction.split(" ")
            if len(temp_ins_list) > 1:
                dst_temp = int(temp_ins_list[2])
                src1_temp = int(temp_ins_list[3])
                src2_temp = int(temp_ins_list[4])

                if dst_temp == 0:
                    dst_temp = self.ZERO_REPLACEMENT

                if src1_temp == 0:
                    src1_temp = self.ZERO_REPLACEMENT

                if src2_temp == 0:
                    src2_temp = self.ZERO_REPLACEMENT

                self.fake_rob_queue.append({
                    "index": index,
                    "tag": temp_ins_list[0],
                    "operation_type": int(temp_ins_list[1]),
                    "dst": dst_temp,
                    "src1": src1_temp,
                    "src2": src2_temp,
                    "IF_cycle": -1,
                    "IF_duration": -1,
                    "ID_cycle": -1,
                    "ID_duration": -1,
                    "IS_cycle": -1,
                    "IS_duration": -1,
                    "EX_cycle": -1,
                    "EX_duration": -1,
                    "WB_cycle": -1,
                    "WB_duration": -1,
                    "current_state": None,
                    "ready": False,
                    "execution_timer": -1
                })
                index = index + 1

        self.instruction_count = len(self.fake_rob_queue)

    def pop(self):
        if self.currIndex + 1 < self.instruction_count:
            index = self.currIndex
            self.currIndex = self.currIndex + 1
            return self.fake_rob_queue[index]
        else:
            return None


class Sim:
    IF = "IF"
    ID = "ID"
    IS = "IS"
    EX = "EX"
    WB = "WB"

    EXECUTE_CYCLE_LATENCY_DICT = {0: 1, 1: 2, 2: 5}

    def __init__(self, data, scheduling_queue_size, peak_fetch_dispatch_issue_rate):
        self.currentCycle = 0
        self.fakeRob = FakeRob(data)
        self.scheduling_queue_size = scheduling_queue_size
        self.peak_fetch_dispatch_issue_rate = peak_fetch_dispatch_issue_rate
        self.fetch_list = []
        self.dispatch_list = []
        self.issue_list = []
        self.execute_list = []
        self.writeback_list = []
        self.register_state = {}
        self.reservation_station = {}
        self.epoch = 0

    def print_list(self, state_List):
        for state in state_List:
            print(state)

    def get_formatted_output(self):
        output_array = []
        output = open("output.txt", "w")
        Simulator.fakeRob.fake_rob_queue.pop()
        for data in Simulator.fakeRob.fake_rob_queue:
            dst_temp = int(data["dst"])
            src1_temp = int(data["src1"])
            src2_temp = int(data["src2"])

            if dst_temp == Simulator.fakeRob.ZERO_REPLACEMENT:
                dst_temp = 0

            if src1_temp == Simulator.fakeRob.ZERO_REPLACEMENT:
                src1_temp = 0

            if src2_temp == Simulator.fakeRob.ZERO_REPLACEMENT:
                src2_temp = 0
            output_array.append((str(data["index"] - 1) +
                                 " fu{" + str(data["operation_type"])
                                 + "} src{" + str(src1_temp) + "," + str(src2_temp)
                                 + "} dst{" + str(dst_temp)
                                 + "} IF{" + str(data["IF_cycle"]) + "," + str(data["IF_duration"])
                                 + "} ID{" + str(data["ID_cycle"]) + "," + str(data["ID_duration"])
                                 + "} IS{" + str(data["IS_cycle"]) + "," + str(data["IS_duration"])
                                 + "} EX{" + str(data["EX_cycle"]) + "," + str(data["EX_duration"])
                                 + "} WB{" + str(data["WB_cycle"]) + "," + str(data["WB_duration"]) + "}"))

            print(str(data["index"] - 1) +
                  " fu{" + str(data["operation_type"])
                  + "} src{" + str(src1_temp) + "," + str(src2_temp)
                  + "} dst{" + str(dst_temp)
                  + "} IF{" + str(data["IF_cycle"]) + "," + str(data["IF_duration"])
                  + "} ID{" + str(data["ID_cycle"]) + "," + str(data["ID_duration"])
                  + "} IS{" + str(data["IS_cycle"]) + "," + str(data["IS_duration"])
                  + "} EX{" + str(data["EX_cycle"]) + "," + str(data["EX_duration"])
                  + "} WB{" + str(data["WB_cycle"]) + "," + str(data["WB_duration"]) + "}")

            output.write((str(data["index"] - 1) +
                          " fu{" + str(data["operation_type"])
                          + "} src{" + str(src1_temp) + "," + str(src2_temp)
                          + "} dst{" + str(dst_temp)
                          + "} IF{" + str(data["IF_cycle"]) + "," + str(data["IF_duration"])
                          + "} ID{" + str(data["ID_cycle"]) + "," + str(data["ID_duration"])
                          + "} IS{" + str(data["IS_cycle"]) + "," + str(data["IS_duration"])
                          + "} EX{" + str(data["EX_cycle"]) + "," + str(data["EX_duration"])
                          + "} WB{" + str(data["WB_cycle"]) + "," + str(data["WB_duration"]) + "}") + "\n")

        # Close the file
        output.close()

    def validate_file(self, txtFile):
        file = open(txtFile, "r")
        lines = file.readlines()
        index = 0
        test = 0
        for data in Simulator.fakeRob.fake_rob_queue:
            dst_temp = int(data["dst"])
            src1_temp = int(data["src1"])
            src2_temp = int(data["src2"])

            if dst_temp == Simulator.fakeRob.ZERO_REPLACEMENT:
                dst_temp = 0

            if src1_temp == Simulator.fakeRob.ZERO_REPLACEMENT:
                src1_temp = 0

            if src2_temp == Simulator.fakeRob.ZERO_REPLACEMENT:
                src2_temp = 0

            our_line = (str(data["index"] - 1) +
                        " fu{" + str(data["operation_type"])
                        + "} src{" + str(src1_temp) + "," + str(src2_temp)
                        + "} dst{" + str(dst_temp)
                        + "} IF{" + str(data["IF_cycle"]) + "," + str(data["IF_duration"])
                        + "} ID{" + str(data["ID_cycle"]) + "," + str(data["ID_duration"])
                        + "} IS{" + str(data["IS_cycle"]) + "," + str(data["IS_duration"])
                        + "} EX{" + str(data["EX_cycle"]) + "," + str(data["EX_duration"])
                        + "} WB{" + str(data["WB_cycle"]) + "," + str(data["WB_duration"]) + "}")

            if (our_line != lines[index].strip()):
                print("Ours")
                print(our_line)
                print("Expected")
                print(lines[index].strip())
                test += 1
                # break
            index = index + 1
        print("# Wrong FU's", test)

    def is_reservation_station_instruction_ready(self, instruction):
        reservation_item = self.reservation_station[instruction["index"]]

        if reservation_item["QJ"] == -1 and reservation_item["QK"] == -1:
            return True
        else:
            valid = True

            if (reservation_item["QJ"] != -1):
                value = self.reservation_station.get(reservation_item["QJ"])
                if (value != None):
                    valid = False
                # else:
                #    print("Cycle: " + str(self.currentCycle) + " Index was not updated: " + str(reservation_item["QJ"]) + " in instruction: " + str(instruction["index"]))

            if (reservation_item["QK"] != -1):
                value = self.reservation_station.get(reservation_item["QK"])
                if (value != None):
                    valid = False
                # else:
                #    print("Cycle: " + str(self.currentCycle) + " Index was not updated: " + str(reservation_item["QK"]) + " in instruction: " + str(instruction["index"]))

            return valid
    def add_instruction_reservation_station(self, instruction):
        value = self.reservation_station.get(instruction["index"])
        VJ = -1
        VK = -1
        QJ = -1
        QK = -1

        if value is None:
            if self.register_state.get(instruction["dst"]) is None:
                self.update_register_state(instruction["dst"], instruction["index"])
                # The dst of this instruction is mapped to a register. Therefore, the instruction has been executed
                # then that register is ready to be retrieved marked by -1.

            QJ = (instruction["src1"])
            QK = (instruction["src2"])

            self.reservation_station[instruction["index"]] = {
                "OP": instruction["operation_type"],
                "VJ": VJ,
                "VK": VK,
                "QJ": QJ,
                "QK": QK
            }

    def update_register_state(self, register, index):
        if register == -1:
            return
        else:
            self.register_state[register] = register, index

    def fake_retire(self):
        for writeback_instruction in self.writeback_list:
            if (writeback_instruction["WB_cycle"] == -1):
                writeback_instruction["WB_cycle"] = self.currentCycle

            writeback_instruction["current_state"] = Sim.WB

        while len(self.writeback_list) != 0:
            writeback_instruction = self.writeback_list.pop()
            writeback_instruction["WB_duration"] = 1
            writeback_instruction["WB_cycle"] = self.currentCycle
            dst = self.register_state.get(writeback_instruction["dst"])
            if (dst is not None):
                if (writeback_instruction["index"] == dst[1]):
                    # Make sure that you only allow 0 to 127 registers
                    self.update_register_state(writeback_instruction["dst"], -1)

        return

    def execute(self):
        # From the issue_list, construct a temp list of instructions whose
        # operands are ready – these are the READY instructions.

        # Execute instructions
        for execute_instruction in self.execute_list:
            if (execute_instruction["EX_cycle"] == -1):
                execute_instruction["EX_cycle"] = self.currentCycle

            execute_instruction["current_state"] = Sim.EX
            execute_instruction["ready"] = False

        ready_list = []
        for execute_instruction in self.execute_list:
            if self.is_ready(execute_instruction):
                execute_instruction["ready"] = True
                execute_instruction["EX_duration"] = Sim.EXECUTE_CYCLE_LATENCY_DICT[
                    execute_instruction["operation_type"]]

                ready_list.append(execute_instruction)

        for ready_instruction in ready_list:
            self.writeback_list.append(ready_instruction)
            self.execute_list.remove(ready_instruction)
            del self.reservation_station[ready_instruction["index"]]

        return

    def is_ready(self, execute_instruction):
        src1_is_ready = False
        src2_is_ready = False
        dst = self.register_state.get(execute_instruction["dst"])
        if execute_instruction["src1"] != -1:
            src1 = self.register_state.get(execute_instruction["src1"])
            if src1 is not None:
                if src1[1] == -1:
                    src1_is_ready = True
                if dst is not None and (dst[0] == src1[0] and dst[1] == execute_instruction["index"]):
                    src1_is_ready = True
            else:
                src1_is_ready = True
        else:
            src1_is_ready = True

        if execute_instruction["src2"] != -1:
            src2 = self.register_state.get(execute_instruction["src2"])
            if src2 is not None:
                if src2[1] == -1:
                    src2_is_ready = True
                if dst is not None and (dst[0] == src2[0] and dst[1] == execute_instruction["index"]):
                    src2_is_ready = True
            else:
                src2_is_ready = True
        else:
            src2_is_ready = True
        return src1_is_ready and src2_is_ready

    def issue(self):
        # Issue instructions
        for issue_instruction in self.issue_list:
            if issue_instruction["IS_cycle"] == -1:
                issue_instruction["IS_cycle"] = self.currentCycle
                issue_instruction["current_state"] = Sim.IS

        temp_list = sorted(self.issue_list, key=lambda d: d["index"])
        self.issue_list = temp_list

        for issue_instruction in self.issue_list:
            if len(self.reservation_station) <= self.scheduling_queue_size:
                self.add_instruction_reservation_station(issue_instruction)

        ready_list = []
        execution_cap = self.peak_fetch_dispatch_issue_rate + 9999 - len(self.execute_list)

        # Need to investigate or change logic to fit files
        for issue_instruction in self.issue_list:
            value = self.reservation_station.get(issue_instruction["index"])
            # Need to verify
            if execution_cap > 0 and value is not None and len(self.reservation_station) <= self.scheduling_queue_size:
                ready_list.append(issue_instruction)
                execution_cap = execution_cap - 1

        for ready_instruction in ready_list:
            ready_instruction["execution_timer"] = self.currentCycle + Sim.EXECUTE_CYCLE_LATENCY_DICT[
                ready_instruction["operation_type"]]
            # Calcuating wrong time - could be ready_instruction list is not correct
            ready_instruction["IS_duration"] = self.currentCycle + 1 - ready_instruction["IS_cycle"]
            # Somehow the same instructions are getting added
            if ready_instruction not in self.execute_list:
                self.execute_list.append(ready_instruction)
            self.issue_list.remove(ready_instruction)

        return

    def dispatch(self):
        # Dispatch instructions
        to_remove = []
        for dispatch_instruction in self.dispatch_list:

            if (dispatch_instruction["ID_cycle"] == -1):
                dispatch_instruction["ID_cycle"] = self.currentCycle
                dispatch_instruction["current_state"] = Sim.ID

            if (dispatch_instruction["current_state"] == Sim.IS):
                to_remove.append(dispatch_instruction)

        for rm_instruction in to_remove:
            self.dispatch_list.remove(rm_instruction)

        ready_list = []
        issue_cap = 0

        issue_cap = self.scheduling_queue_size - len(self.issue_list)

        for dispatch_instruction in self.dispatch_list:

            if issue_cap == 0:
                break

            ready_list.append(dispatch_instruction)

            issue_cap = issue_cap - 1

        for ready_instruction in ready_list:
            ready_instruction["ID_duration"] = self.currentCycle + 1 - ready_instruction["ID_cycle"]
            self.issue_list.append(ready_instruction)
            # self.dispatch_list.remove(ready_instruction)

        return

    def fetch(self):
        # Fetch instructions
        while len(self.fetch_list) < self.peak_fetch_dispatch_issue_rate:
            instruction_fetched = self.fakeRob.pop()
            if instruction_fetched == None:
                break
            else:
                self.fetch_list.append(instruction_fetched)

        maxSendCount = min(self.peak_fetch_dispatch_issue_rate,
                           (self.peak_fetch_dispatch_issue_rate) * 2 - len(self.dispatch_list))

        for i in range(0, maxSendCount):
            if len(self.fetch_list) > 0:
                instruction_fetched = self.fetch_list[0]
                self.dispatch_list.append(instruction_fetched)
                instruction_fetched["IF_cycle"] = self.currentCycle
                instruction_fetched["current_state"] = Sim.IF
                instruction_fetched["IF_duration"] = 1
                self.fetch_list.remove(instruction_fetched)

        return

    def advance_cycle(self):

        debug_cycle = 2
        self.epoch += 1
        if self.currentCycle == debug_cycle:
            print("Current Cycle: " + str(self.currentCycle))
            # print("Register State")
            # print(self.register_state)
            print("Execution Count: " + str(len(self.execute_list)))
            print("Reservation Count: " + str(len(self.reservation_station.keys())))
            print("Issue Count: " + str(len(self.issue_list)))
            print("Dispatch Count: " + str(len(self.dispatch_list)))
            print("fetch Count: " + str(len(self.fetch_list)))
            # print("Schedule Window Count: " + str(len(self.re)))
            # self.PrintList(self.issue_list)

        # self.PrintList(self.execute_list)

        if (self.currentCycle == debug_cycle):
            print("____Reservation Debug___")
            print("Current Cycle: " + str(self.currentCycle))
            print("Reservation Station")
            print(self.reservation_station)
            print("Register State")
            print(self.register_state)
            print("____Reservation Debug End___")

            for issue_instruction in self.issue_list:
                if (issue_instruction["index"] == 1136):
                    print("Instruction is ready: " + str(
                        self.is_reservation_station_instruction_ready(issue_instruction)))

        self.currentCycle = self.currentCycle + 1

        # self.DebugPrintList(self.dispatch_list)

        if len(self.fetch_list) == 0 and len(self.dispatch_list) == 0 and len(self.issue_list) == 0 and len(
                self.execute_list) == 0 and len(self.writeback_list) == 0:
            return False
        else:
            return True

    def main(self):
        epoch = 1
        while True:
            self.fake_retire()
            self.execute()
            self.issue()
            self.dispatch()
            self.fetch()

            if (self.advance_cycle() == False):
                print("End Of Sim")
                break
            epoch += 1


# In[27]:

def debug_print_list(self, listToPrint):
    print([i["index"] for i in listToPrint])


def read_file(txtFile):
    file = open(txtFile, "r")
    lines = file.readlines()
    data_string = ""
    for line in lines:
        data_string += line

    return data_string + "FFFFF -1 -1 -1 -1\n"


# In[36]:

# Need to add funcationlity that takes in inputs.Need to add funcationlity that takes in inputs.
data = read_file("val_trace_perl.txt")
Simulator = Sim(data, 128, 8)

# In[37]:


Simulator.main()
Simulator.validate_file("pipe_128_8_perl.txt")

# In[38]:
# Simulator.get_formatted_output()

# In[ ]:


# In[ ]:
