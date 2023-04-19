#!/usr/bin/env python
# coding: utf-8

import sys


class FakeRob:
    def __init__(self, instruction_list_string):
        self.fake_rob_queue = []
        self.currIndex = 0
        data_string = instruction_list_string.split("\n")
        index = 0
        for instruction in data_string:
            temp_ins_list = instruction.split(" ")
            if len(temp_ins_list) > 1:
                dst_temp = int(temp_ins_list[2])
                src1_temp = int(temp_ins_list[3])
                src2_temp = int(temp_ins_list[4])

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
        self.ready = []
        self.currentCycle = 0
        self.fakeRob = FakeRob(data)
        self.scheduling_queue_size = scheduling_queue_size
        self.peak_fetch_dispatch_issue_rate = peak_fetch_dispatch_issue_rate
        self.dispatch_list = []
        self.issue_list = []
        self.execute_list = []
        self.register_state = {}
        self.reservation_station = {}
        self.epoch = 0

    def print_list(self, state_list):
        for state in state_list:
            print(state)

    def get_formatted_output(self):
        output_array = []
        output = open("../src/output.txt", "w")
        Simulator.fakeRob.fake_rob_queue.pop()
        for data in Simulator.fakeRob.fake_rob_queue:
            dst_temp = int(data["dst"])
            src1_temp = int(data["src1"])
            src2_temp = int(data["src2"])

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


    def validate_file(self, txt_file):
        file = open(txt_file, "r")
        lines = file.readlines()
        index = 0
        test = 0
        for data in Simulator.fakeRob.fake_rob_queue:
            dst_temp = int(data["dst"])
            src1_temp = int(data["src1"])
            src2_temp = int(data["src2"])

            our_line = (str(data["index"]) +
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
                if test == 5:
                    break
            index = index + 1

    # print("# Wrong FU's", test)

    def add_instruction_reservation_station(self, instruction):
        value = self.reservation_station.get(instruction["index"])

        qj = -1
        qk = -1

        if value is None:
            if self.check_register_state(instruction["src1"]) is not False:
                qj = self.check_register_state(instruction["src1"])
            else:
                qj = instruction["src1"], instruction["index"]

            if self.check_register_state(instruction["src2"]) is not False:
                qk = self.check_register_state(instruction["src2"])
            else:
                qk = instruction["src2"], instruction["index"]

            self.update_register_state(instruction["dst"], instruction["index"])

            self.reservation_station[instruction["index"]] = {
                "op": instruction["operation_type"],
                "qj": qj,
                "qk": qk
            }

    # Need to update to prevent duplicate register values from overwriting each other.
    def update_register_state(self, register, index):
        if register == -1:
            return
        else:
            self.register_state[register] = register, index

    def check_register_state(self, register):
        if register == -1:
            return False

        value = self.register_state.get(register)

        if value is None:
            return False
        else:
            return value

    def fake_retire(self):
        # Remove instructions
        # from the head of the fake - ROB
        # until an instruction is reached that is not in the WB state.
        return

    def execute(self):
        # Execute instructions
        to_remove = []
        for execute_instruction in self.execute_list:
            if execute_instruction["execution_timer"] == self.currentCycle:
                execute_instruction["EX_duration"] = self.currentCycle - execute_instruction["EX_cycle"] + 1
                execute_instruction["current_state"] = Sim.WB
                execute_instruction["WB_duration"] = 1
                execute_instruction["WB_cycle"] = self.currentCycle + 1
                if execute_instruction["index"] == self.check_register_state(execute_instruction["dst"]):
                    self.update_register_state(execute_instruction["dst"], -1)
                to_remove.append(execute_instruction)
        for item in to_remove:
            self.execute_list.remove(item)

        return

    def is_ready(self, execute_instruction):
        rs = self.reservation_station[execute_instruction["index"]]
        src1_ready = False
        src2_ready = False

        qj = self.check_register_state(rs["qj"])
        qk = self.check_register_state(rs["qk"])

        if rs is not None:
            if qj[1] == execute_instruction["index"] or qj[1] == -1:
                src1_ready = True
            if qk[1] == execute_instruction["index"] or qk[1] == -1:
                src2_ready = True

        return src1_ready and src2_ready

    def issue(self):
        # Issue instructions
        temp_list = sorted(self.issue_list, key=lambda d: d["tag"])

        for issue_instruction in temp_list:
            value = self.reservation_station.get(issue_instruction["index"])
            if value is not None and self.is_ready(issue_instruction):
                self.issue_list.remove(issue_instruction)
                issue_instruction["execution_timer"] = self.currentCycle + Sim.EXECUTE_CYCLE_LATENCY_DICT[
                    issue_instruction["operation_type"]]
                issue_instruction["IS_duration"] = self.currentCycle - issue_instruction["IS_cycle"] + 1
                issue_instruction["current_state"] = Sim.EX
                issue_instruction["EX_cycle"] = self.currentCycle + 1
                self.execute_list.append(issue_instruction)
                del self.reservation_station[issue_instruction["index"]]
        return

    def dispatch(self):
        # Dispatch instructions
        temp_list = sorted(self.dispatch_list, key=lambda d: d["tag"])

        for dispatch_instruction in temp_list:
            if len(self.issue_list) < self.scheduling_queue_size:
                if dispatch_instruction["current_state"] == Sim.IF:
                    dispatch_instruction["ID_cycle"] = self.currentCycle
                    dispatch_instruction["current_state"] = Sim.ID
                    dispatch_instruction["ID_duration"] = self.currentCycle - dispatch_instruction["ID_cycle"] + 1
                    self.dispatch_list.remove(dispatch_instruction)
                    dispatch_instruction["IS_cycle"] = self.currentCycle + 1
                    self.issue_list.append(dispatch_instruction)
                    self.add_instruction_reservation_station(dispatch_instruction)
        return

    def fetch(self):
        # Fetch instructions
        while len(self.dispatch_list) < self.peak_fetch_dispatch_issue_rate:
            instruction_fetched = self.fakeRob.pop()
            if instruction_fetched is None:
                break
            else:
                instruction_fetched["IF_cycle"] = self.currentCycle
                instruction_fetched["current_state"] = Sim.IF
                instruction_fetched["IF_duration"] = 1
                self.dispatch_list.append(instruction_fetched)
                # Possilby create a dispatch queue counter

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
            # print("Schedule Window Count: " + str(len(self.re)))
            # self.PrintList(self.issue_list)

        # self.PrintList(self.execute_list)

        if self.currentCycle == debug_cycle:
            print("____Reservation Debug___")
            print("Current Cycle: " + str(self.currentCycle))
            print("Reservation Station")
            print(self.reservation_station)
            print("Register State")
            print(self.register_state)
            print("____Reservation Debug End___")

        self.currentCycle = self.currentCycle + 1

        if len(self.dispatch_list) == 0 and len(self.issue_list) == 0 and len(
                self.execute_list) == 0:
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


def read_file(txt_file):
    file = open(txt_file, "r")
    lines = file.readlines()
    data_string = ""
    for line in lines:
        data_string += line

    return data_string + "FFFFF -1 -1 -1 -1\n"


# In[36]:

# Need to add funcationlity that takes in inputs.Need to add funcationlity that takes in inputs.
data = read_file("val_trace_gcc.txt")
Simulator = Sim(data, 8, 8)

# In[37]:


Simulator.main()
Simulator.validate_file("pipe_8_8_gcc.txt")

# In[38]:
# Simulator.get_formatted_output()

# In[ ]:


# In[ ]:
