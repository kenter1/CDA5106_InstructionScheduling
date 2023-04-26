#!/usr/bin/env python
# coding: utf-8
from ReservationStation import ReservationStation


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


def is_ready(rs):
    src1_ready = False
    src2_ready = False

    if rs.rs1 is None or rs.rs1 == -1 or rs.val1 is not None:
        src1_ready = True
    if rs.rs2 is None or rs.rs2 == -1 or rs.val2 is not None:
        src2_ready = True

    return src1_ready and src2_ready


def print_list(state_list):
    for state in state_list:
        print(state)


def get_formatted_output():
    output_array = []
    output = open("../src/output.txt", "w")
    Simulator.fakeRob.fake_rob_queue.pop()
    for instr in Simulator.fakeRob.fake_rob_queue:
        dst_temp = int(instr["dst"])
        src1_temp = int(instr["src1"])
        src2_temp = int(instr["src2"])

        output_array.append((str(instr["index"] - 1) +
                             " fu{" + str(instr["operation_type"])
                             + "} src{" + str(src1_temp) + "," + str(src2_temp)
                             + "} dst{" + str(dst_temp)
                             + "} IF{" + str(instr["IF_cycle"]) + "," + str(instr["IF_duration"])
                             + "} ID{" + str(instr["ID_cycle"]) + "," + str(instr["ID_duration"])
                             + "} IS{" + str(instr["IS_cycle"]) + "," + str(instr["IS_duration"])
                             + "} EX{" + str(instr["EX_cycle"]) + "," + str(instr["EX_duration"])
                             + "} WB{" + str(instr["WB_cycle"]) + "," + str(instr["WB_duration"]) + "}"))

        print(str(instr["index"] - 1) +
              " fu{" + str(instr["operation_type"])
              + "} src{" + str(src1_temp) + "," + str(src2_temp)
              + "} dst{" + str(dst_temp)
              + "} IF{" + str(instr["IF_cycle"]) + "," + str(instr["IF_duration"])
              + "} ID{" + str(instr["ID_cycle"]) + "," + str(instr["ID_duration"])
              + "} IS{" + str(instr["IS_cycle"]) + "," + str(instr["IS_duration"])
              + "} EX{" + str(instr["EX_cycle"]) + "," + str(instr["EX_duration"])
              + "} WB{" + str(instr["WB_cycle"]) + "," + str(instr["WB_duration"]) + "}")

        output.write((str(instr["index"] - 1) +
                      " fu{" + str(instr["operation_type"])
                      + "} src{" + str(src1_temp) + "," + str(src2_temp)
                      + "} dst{" + str(dst_temp)
                      + "} IF{" + str(instr["IF_cycle"]) + "," + str(instr["IF_duration"])
                      + "} ID{" + str(instr["ID_cycle"]) + "," + str(instr["ID_duration"])
                      + "} IS{" + str(instr["IS_cycle"]) + "," + str(instr["IS_duration"])
                      + "} EX{" + str(instr["EX_cycle"]) + "," + str(instr["EX_duration"])
                      + "} WB{" + str(instr["WB_cycle"]) + "," + str(instr["WB_duration"]) + "}") + "\n")


def validate_file(txt_file):
    file = open(txt_file, "r")
    lines = file.readlines()
    index = 0
    test = 0
    for instr in Simulator.fakeRob.fake_rob_queue:
        dst_temp = int(instr["dst"])
        src1_temp = int(instr["src1"])
        src2_temp = int(instr["src2"])

        our_line = (str(instr["index"]) +
                    " fu{" + str(instr["operation_type"])
                    + "} src{" + str(src1_temp) + "," + str(src2_temp)
                    + "} dst{" + str(dst_temp)
                    + "} IF{" + str(instr["IF_cycle"]) + "," + str(instr["IF_duration"])
                    + "} ID{" + str(instr["ID_cycle"]) + "," + str(instr["ID_duration"])
                    + "} IS{" + str(instr["IS_cycle"]) + "," + str(instr["IS_duration"])
                    + "} EX{" + str(instr["EX_cycle"]) + "," + str(instr["EX_duration"])
                    + "} WB{" + str(instr["WB_cycle"]) + "," + str(instr["WB_duration"]) + "}")

        if our_line != lines[index].strip():
            print("Ours")
            print(our_line)
            print("Expected")
            print(lines[index].strip())
            test += 1
            if test == 7:
                break
        index = index + 1

    #print("# Wrong FU's", test)


class Sim:
    IF = "IF"
    ID = "ID"
    IS = "IS"
    EX = "EX"
    WB = "WB"

    EXECUTE_CYCLE_LATENCY_DICT = {0: 1, 1: 2, 2: 5}

    def __init__(self, instr, scheduling_queue_size, peak_fetch_dispatch_issue_rate):
        self.ready = []
        self.currentCycle = 0
        self.fakeRob = FakeRob(instr)
        self.scheduling_queue_size = scheduling_queue_size
        self.peak_fetch_dispatch_issue_rate = peak_fetch_dispatch_issue_rate
        self.dispatch_list = []
        self.issue_list = []
        self.execute_list = []
        self.register_state = {}
        self.epoch = 0

    def add_instruction_reservation_station(self, instruction):
        # Pass in instruction to rs. Check and see if register has
        # operand and if so pass it on to rs. If not pass in rs in the
        # register to the rs1 or rs2 values.
        val1 = None
        val2 = None
        rs1 = None
        rs2 = None

        # Get RS with the highest index
        src1 = self.check_reservation_stations(instruction["src1"])
        src2 = self.check_reservation_stations(instruction["src2"])

        if src1 is None:
            val1 = instruction["src1"]
        else:
            rs1 = src1

        if src2 is None:
            val2 = instruction["src2"]
        else:
            rs2 = src2

        rs = ReservationStation(instruction, rs1, rs2, val1, val2)
        self.issue_list.append(rs)
        self.update_register_state(instruction["dst"], rs)

    def update_register_state(self, register, value):
        if register == -1:
            return
        else:
            self.register_state[register] = value

    def check_register_state(self, register):
        if register == -1:
            return -1

        value = self.register_state.get(register)
        return value

    def fake_retire(self):
        # Remove instructions
        # from the head of the fake - ROB
        # until an instruction is reached that is not in the WB state.
        return

    def execute(self):
        # Execute instructions
        to_remove = []
        for rs in self.execute_list:
            if rs.instruction["execution_timer"] == self.currentCycle:
                rs.instruction["EX_duration"] = self.currentCycle - rs.instruction["EX_cycle"] + 1
                rs.instruction["current_state"] = Sim.WB
                rs.instruction["WB_duration"] = 1
                rs.instruction["WB_cycle"] = self.currentCycle + 1
                # When instruction executes check remove instructions from register file
                reg = self.check_register_state(rs.instruction["dst"])
                if reg is not None and reg != -1:
                    del self.register_state[rs.instruction["dst"]]
                # Alert reservation stations
                self.update_reservation_stations(rs)
                to_remove.append(rs)

        for item in to_remove:
            self.execute_list.remove(item)

    def update_reservation_stations(self, rs):
        # If a rs1 matches a rs in an issue list
        # and a rs2 matches a rs in an issue list
        for issue_rs in self.issue_list:
            if issue_rs.rs1 == rs:
                issue_rs.rs1 = None
            if issue_rs.rs2 == rs:
                issue_rs.rs2 = None

    def check_reservation_stations(self, operand):
        # If a rs1 matches a rs in an issue list
        # and a rs2 matches a rs in an issue list
        issue_ex_list = self.execute_list + self.issue_list
        if len(issue_ex_list) > 0:
            temp_list = sorted(issue_ex_list, key=lambda d: d.rs_id, reverse=True)
            if operand == -1:
                return None
            for issue_rs in temp_list:
                if issue_rs.instruction["dst"] == operand:
                    return issue_rs

    def issue(self):
        # Issue instructions
        temp_list = sorted(self.issue_list, key=lambda d: d.rs_id)
        i = 0
        for rs in temp_list:
            if is_ready(rs) and i < self.peak_fetch_dispatch_issue_rate + 1:
                self.issue_list.remove(rs)
                rs.instruction["execution_timer"] = self.currentCycle + Sim.EXECUTE_CYCLE_LATENCY_DICT[
                    rs.instruction["operation_type"]]
                rs.instruction["IS_duration"] = self.currentCycle - rs.instruction["IS_cycle"] + 1
                rs.instruction["current_state"] = Sim.EX
                rs.instruction["EX_cycle"] = self.currentCycle + 1
                self.execute_list.append(rs)
            i = i + 1

    def dispatch(self):
        # Dispatch instructions
        # Add to the Dispatch queue/ID state first - Put in fetch method
        # Then next cycle check if ready for Issue queue/state - Add check each cycle if in ID
        i = 0
        temp_list = sorted(self.dispatch_list, key=lambda d: d["index"])
        for dispatch_instruction in temp_list:
            if dispatch_instruction["ID_cycle"] == -1:
                dispatch_instruction["ID_cycle"] = self.currentCycle
            if len(self.issue_list) < self.scheduling_queue_size and i < self.peak_fetch_dispatch_issue_rate:
                if dispatch_instruction["current_state"] == Sim.ID:
                    dispatch_instruction["current_state"] = Sim.IS
                    dispatch_instruction["ID_duration"] = self.currentCycle - dispatch_instruction["ID_cycle"] + 1
                    dispatch_instruction["IS_cycle"] = self.currentCycle + 1
                    self.add_instruction_reservation_station(dispatch_instruction)
                    self.dispatch_list.remove(dispatch_instruction)
            i = i + 1

    def fetch(self):
        # Fetch instructions
        i = 0
        while i < self.peak_fetch_dispatch_issue_rate \
                and len(self.dispatch_list) < self.peak_fetch_dispatch_issue_rate * 2:
            instruction_fetched = self.fakeRob.pop()
            if instruction_fetched is None:
                break
            else:
                instruction_fetched["IF_cycle"] = self.currentCycle
                instruction_fetched["current_state"] = Sim.ID
                instruction_fetched["IF_duration"] = 1
                self.dispatch_list.append(instruction_fetched)
                # Possilby create a dispatch queue counter
            i = i + 1

    def advance_cycle(self):
        debug_cycle = 2
        self.epoch += 1
        if self.currentCycle == debug_cycle:
            print("Current Cycle: " + str(self.currentCycle))
            # print("Register State")
            # print(self.register_state)
            print("Execution Count: " + str(len(self.execute_list)))
            print("Issue Count: " + str(len(self.issue_list)))
            print("Dispatch Count: " + str(len(self.dispatch_list)))
            # print("Schedule Window Count: " + str(len(self.re)))
            # self.PrintList(self.issue_list)

        # self.PrintList(self.execute_list)

        if self.currentCycle == debug_cycle:
            print("____Reservation Debug___")
            print("Current Cycle: " + str(self.currentCycle))
            print("Reservation Station")
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

            if not self.advance_cycle():
                print("End Of Sim")
                break
            epoch += 1


def debug_print_list(list_to_print):
    print([i["index"] for i in list_to_print])


def read_file(txt_file):
    file = open(txt_file, "r")
    lines = file.readlines()
    data_string = ""
    for line in lines:
        data_string += line

    return data_string + "FFFFF -1 -1 -1 -1\n"


# Need to add functionality that takes in inputs.Need to add functionality that takes in inputs.
data = read_file("val_trace_gcc.txt")
Simulator = Sim(data, 8, 8)

Simulator.main()
validate_file("pipe_8_8_gcc.txt")
