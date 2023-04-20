class ReservationStation:
    def __init__(self, instruction, rs1, rs2, val1, val2):
        self.rs_id = instruction["index"]
        self.op = instruction["operation_type"]
        self.rs1 = rs1
        self.rs2 = rs2
        self.val1 = val1
        self.val2 = val2
        self.instruction = instruction

        # Maybe add busy property

