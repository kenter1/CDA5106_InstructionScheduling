import sys

class FakeROB:

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
                    "index":index,
                    "tag":temp_ins_list[0],
                    "operation_type": int(temp_ins_list[1]),
                    "dst": dst_temp,
                    "src1": src1_temp,
                    "src2": src2_temp,
                    "IF_cycle":-1,
                    "IF_duration":-1,
                    "ID_cycle":-1,
                    "ID_duration":-1,
                    "IS_cycle":-1,
                    "IS_duration":-1,
                    "EX_cycle":-1,
                    "EX_duration":-1,
                    "WB_cycle":-1,
                    "WB_duration":-1,
                    "current_state":None,
                    "ready": False,
                    "execution_timer":-1
                })
                index = index + 1
                
        self.instruction_count = len(self.fake_rob_queue)
    
    def Pop(self):
        
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
    
    EXECUTE_CYCLE_LATENCY_DICT = {0:1, 1:2, 2:5}
    
    def __init__(self, data,scheduling_queue_size, peak_fetch_dispatch_issue_rate):
        self.currentCycle = 0
        self.fakeRob = FakeROB(data)
        self.scheduling_queue_size = scheduling_queue_size
        self.peak_fetch_dispatch_issue_rate = peak_fetch_dispatch_issue_rate
        self.fetch_list = []
        self.dispatch_list = []
        self.issue_list = []
        self.execute_list = []
        self.writeback_list = []
        self.register_state = {}
        self.reservation_station = {}
     
    
    def PrintList(self, state_List):
        for state in state_List:
            print(state)
    
    def GetFormattedOutput(self):
        for i in range(0, len(simulator.fakeRob.fake_rob_queue) - 1):
            data = simulator.fakeRob.fake_rob_queue[i]
            dst_temp = int(data["dst"])
            src1_temp = int(data["src1"])
            src2_temp = int(data["src2"])
                
            if dst_temp == simulator.fakeRob.ZERO_REPLACEMENT:
                dst_temp = 0
            
            if src1_temp == simulator.fakeRob.ZERO_REPLACEMENT:
                src1_temp = 0
                    
            if src2_temp == simulator.fakeRob.ZERO_REPLACEMENT:
                src2_temp = 0
            
            
            print( str(data["index"] - 1) + 
                  " fu{" + str(data["operation_type"]) 
                  + "} src{" + str(src1_temp) + "," + str(src2_temp) 
                  + "} dst{" + str(dst_temp) 
                  + "} IF{" +  str(data["IF_cycle"]) + "," + str(data["IF_duration"]) 
                  + "} ID{" + str(data["ID_cycle"]) + "," + str(data["ID_duration"])  
                  + "} IS{" + str(data["IS_cycle"]) + "," + str(data["IS_duration"]) 
                  + "} EX{" + str(data["EX_cycle"]) + "," + str(data["EX_duration"])  
                  + "} WB{" + str(data["WB_cycle"]) + "," + str(data["WB_duration"])  + "}")
    
        instruction_count = len(simulator.fakeRob.fake_rob_queue) - 1
        cycle_count = simulator.currentCycle
        print("number of instructions = {}".format(instruction_count))
        print("number of cycles       = {}".format(cycle_count))
        print("IPC                    = {:0.5f}".format(instruction_count/cycle_count))
        
    def IsReservationStationInstructionReady(self, instruction):
        reservation_item = self.reservation_station[instruction["index"]]
        
        if reservation_item["QJ"] == -1 and reservation_item["QK"] == -1:
            return True
        else:
   
            valid = True
            
            if(reservation_item["QJ"] != -1):
                value = self.reservation_station.get(reservation_item["QJ"])
                if(value != None):
                    valid = False
                #else:
                #    print("Cycle: " + str(self.currentCycle) + " Index was not updated: " + str(reservation_item["QJ"]) + " in instruction: " + str(instruction["index"]))
                    
            if(reservation_item["QK"] != -1):
                value = self.reservation_station.get(reservation_item["QK"])
                if(value != None):
                    valid = False
                #else:
                #    print("Cycle: " + str(self.currentCycle) + " Index was not updated: " + str(reservation_item["QK"]) + " in instruction: " + str(instruction["index"]))
            
            return valid
       
    
    def DeleteFromReservationStation(self, instruction):
        del self.reservation_station[instruction["index"]]
        
        #registerValue = self.CheckRegisterState(instruction["dst"])
        #if registerValue != False and registerValue == instruction["index"]:
        #    self.UpdateRegisterState(instruction["index"], False)
        
    def RemoveInstructionReservationStation(self, instruction):
        indexToCleanup = instruction["index"]
        
        self.DeleteFromReservationStation(instruction)
        
        for key in self.reservation_station.keys():
            if(self.reservation_station[key]["QJ"] == indexToCleanup):
                self.reservation_station[key]["QJ"] = -1
                
            if(self.reservation_station[key]["QK"] == indexToCleanup):
                self.reservation_station[key]["QK"] = -1
        
    def AddInstructionReservationStation(self, instruction):
        
        #if(instruction["index"] == 3):
        #    print("Cycle: " + str(self.currentCycle) + " Adding Index: " + str(instruction["index"]))
        
        value = self.reservation_station.get(instruction["index"])
        VJ = -1
        VK = -1
        QJ = -1
        QK = -1
        

        
        if value == None:
            if(self.CheckRegisterState(instruction["src1"]) != False):
                QJ = self.CheckRegisterState(instruction["src1"])
            #else:
                #print("Value of " + str(self.CheckRegisterState(instruction["src1"])))
            
            if(self.CheckRegisterState(instruction["src2"]) != False):
                QK = self.CheckRegisterState(instruction["src2"])
            #else:
                #print("Value of " + str(self.CheckRegisterState(instruction["src2"])))
        
            self.UpdateRegisterState(instruction["dst"], instruction["index"])
            
            
            self.reservation_station[instruction["index"]] = {
                                                           "OP": instruction["operation_type"],
                                                           "VJ":VJ,
                                                           "VK":VK,
                                                           "QJ":QJ,
                                                           "QK":QK
                                                            }
            
    def UpdateRegisterState(self, register, value):
        if register == -1:
            return
        else:
            self.register_state[register] = value
            
    def CheckRegisterState(self, register):
        if register == -1:
            return False
        
        value = self.register_state.get(register)
        
        if value == None:
            return False
        else:
            return value
        
    def FakeRetire(self):
        for writeback_instruction in self.writeback_list:
            if(writeback_instruction["WB_cycle"] == -1):
                writeback_instruction["WB_cycle"] = self.currentCycle
        
            writeback_instruction["current_state"] = Sim.WB
        
        while len(self.writeback_list) != 0:
            writeback_instruction = self.writeback_list.pop()
            writeback_instruction["WB_duration"] = 1
            writeback_instruction["WB_cycle"] = self.currentCycle
            
            if(writeback_instruction["index"] == self.CheckRegisterState(writeback_instruction["dst"])):
                self.UpdateRegisterState(writeback_instruction["dst"], False)

            
        return

    def Execute(self):
        # Execute instructions
        for execute_instruction in self.execute_list:
            if(execute_instruction["EX_cycle"] == -1):
                execute_instruction["EX_cycle"] = self.currentCycle
        
            execute_instruction["current_state"] = Sim.EX
            execute_instruction["ready"] = False
        
        
        ready_list = []
        for execute_instruction in self.execute_list:
            
            #if execute_instruction["EX_cycle"] + Sim.EXECUTE_CYCLE_LATENCY_DICT[execute_instruction["operation_type"]] < self.currentCycle + 2:
            if execute_instruction["execution_timer"] == self.currentCycle:
                #print("Execution Finished at {} in cycle {}".format(str(execute_instruction["index"]), str(self.currentCycle)))
                execute_instruction["ready"] = True
                execute_instruction["EX_duration"] = Sim.EXECUTE_CYCLE_LATENCY_DICT[execute_instruction["operation_type"]]
                
                ready_list.append(execute_instruction)
                
        for ready_instruction in ready_list:

            self.RemoveInstructionReservationStation(ready_instruction)
            self.writeback_list.append(ready_instruction)
            self.execute_list.remove(ready_instruction)
            
                    
        return

    def Issue(self):
        # Issue instructions
                                     
        #if(self.currentCycle == 8):
        #print("At cycle {} value of register state 14 is {}".format(str(self.currentCycle),str(self.CheckRegisterState(14))))
        #print(self.fakeRob.fake_rob_queue[4])
        
        for issue_instruction in self.issue_list:
            
            if(issue_instruction["IS_cycle"] == -1):
                issue_instruction["IS_cycle"] = self.currentCycle
                issue_instruction["current_state"] = Sim.IS
                
        temp_list = sorted(self.issue_list, key=lambda d: d["index"]) 
        self.issue_list = temp_list
        
        for issue_instruction in self.issue_list:
            self.AddInstructionReservationStation(issue_instruction)
        
        ready_list = []
        execution_cap = self.peak_fetch_dispatch_issue_rate + 1 

        for issue_instruction in self.issue_list:
            
            value = self.reservation_station.get(issue_instruction["index"])
            if(execution_cap > 0 and value != None and self.IsReservationStationInstructionReady(issue_instruction) == True):
                ready_list.append(issue_instruction)
                execution_cap = execution_cap - 1
        
        for ready_instruction in ready_list:
            ready_instruction["execution_timer"] = self.currentCycle + Sim.EXECUTE_CYCLE_LATENCY_DICT[ready_instruction["operation_type"]]
            ready_instruction["IS_duration"] = self.currentCycle + 1 - ready_instruction["IS_cycle"]

            self.execute_list.append(ready_instruction)
            self.issue_list.remove(ready_instruction)      
        
        return

    def Dispatch(self):
        # Dispatch instructions
        to_remove = []
        for dispatch_instruction in self.dispatch_list:
            
            if(dispatch_instruction["ID_cycle"] == -1):
                dispatch_instruction["ID_cycle"] = self.currentCycle
                dispatch_instruction["current_state"] = Sim.ID 

                
            if(dispatch_instruction["current_state"] == Sim.IS):
                to_remove.append(dispatch_instruction)
        
        for rm_instruction in to_remove:
            self.dispatch_list.remove(rm_instruction)
        
        ready_list = []
        issue_cap = 0
       
        issue_cap =  self.scheduling_queue_size - len(self.issue_list)
        
        for dispatch_instruction in self.dispatch_list:
            
            if issue_cap == 0:
                break
            
            ready_list.append(dispatch_instruction)
            
            issue_cap = issue_cap - 1
            
        for ready_instruction in ready_list:
            ready_instruction["ID_duration"] = self.currentCycle + 1 - ready_instruction["ID_cycle"]
            self.issue_list.append(ready_instruction)
            #self.dispatch_list.remove(ready_instruction)
            
        return

    def Fetch(self):
        # Fetch instructions
        while len(self.fetch_list) < self.peak_fetch_dispatch_issue_rate:
            instruction_fetched = self.fakeRob.Pop()
            if instruction_fetched == None:
                break
            else:
                self.fetch_list.append(instruction_fetched)
                
        maxSendCount = min(self.peak_fetch_dispatch_issue_rate,  (self.peak_fetch_dispatch_issue_rate) * 2 - len(self.dispatch_list)) 
        
        for i in range(0, maxSendCount):
            if len(self.fetch_list) > 0:
                instruction_fetched = self.fetch_list[0]
                self.dispatch_list.append(instruction_fetched)
                instruction_fetched["IF_cycle"] = self.currentCycle
                instruction_fetched["current_state"] = Sim.IF
                instruction_fetched["IF_duration"] = 1
                self.fetch_list.remove(instruction_fetched)
                

                
        return

    def Advance_Cycle(self):
         
        self.currentCycle = self.currentCycle + 1        

        if len(self.fetch_list) == 0 and len(self.dispatch_list) == 0 and len(self.issue_list) == 0 and len(self.execute_list) == 0 and len(self.writeback_list) == 0:
            return False
        else:
            return True
        
    def Main(self):
        while True:
            self.FakeRetire()
            self.Execute()
            self.Issue()
            self.Dispatch()
            self.Fetch()

            if(self.Advance_Cycle() == False):
                #print("End Of Sim")
                break

def ReadFile(txtFile):
    file = open(txtFile, "r")
    lines = file.readlines()
    data_string = ""
    for line in lines:
        data_string += line
        
    return data_string + "FFFFF -1 -1 -1 -1\n"

if __name__ == "__main__":
    S = int(sys.argv[1])
    N = int(sys.argv[2])
    filename = sys.argv[3]
    data = ReadFile(filename)
    simulator = Sim(data,S,N)
    
    simulator.Main()
    simulator.GetFormattedOutput()