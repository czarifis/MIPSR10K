'''
    Created on Nov 30, 2014

    @author: Costas Zarifis
'''


'''
This class provides all the functionality for decoding instructions
Notes:

    * Logical Registers (ALU Registers): Actual registers appearing within instruction fields
    * Physical Registers : Locations in the actual hardware register file
    * Mapping the logical level to the Physical 
    * ROB == Active list
    * a completed or an incompleted instruction that remains on the reorder buffer 
      must be aborted if it follows an exception or a mispredict branch  
    * 33 logical (1-31 plus hi and lo) and 64 physical integer registers
    * 32 logical (0-31) and 64 physical floating point registers 
    * register map table: unit that maps logical to physical registers
        - 16 read ports (4 instructions x 4 registers)
    * Integer AND FP free lists contain list of currently unassigned physical registers

'''
import Models.Instruction as ins


class Decode:

    def __init__(self):

        self.currInstrs = {}
        self.clc = 0
        self.currDecodedInstrs = {}
        self.currIssuedInstrs = {}

    

    def calc(self, df, instructions, activeList):
        # print 'Decode calc'
        self.currIssuedInstrs = {}
        if instructions is not None:
            # print instructions
            # Inst = ins.Instruction()
            
            # self.currInstrs = instructions

            d4 = dict(self.currInstrs)
            d4.update(instructions)
            self.currInstrs = d4

            self.iterOverInstructions(activeList)
            return self.currDecodedInstrs
        else:
            return None
        
    # This function iterates over 4 instructions at each cycle
    def iterOverInstructions(self,activeList):
        self.currDecodedInstrs = {}
        it = 0
        about_to_be_deleted = []

        for instr in sorted(self.currInstrs):
            (line, actualInstr) = self.currInstrs[instr]
            if line == 39:
                pass

            # print 'Instruction about to get decoded:', actualInstr
            try:
                Inst = ins.Instruction(line, actualInstr)
                Inst.printInstr()

                activeList.process_decode(line, Inst)
                self.currDecodedInstrs[instr] = Inst
                self.currIssuedInstrs[instr] = self.currInstrs[instr]
                about_to_be_deleted.append(line)
                # activeList.process_add2queue(Inst)
                it += 1
                if it == 4:
                    break
            except:
                print 'ROB is full I need to stall the Decode stage', line
                break

        for ii in about_to_be_deleted:
            del self.currInstrs[ii]

            # self.currInstrs[line] = Inst

    def edge(self, df, dfMap, activeList):
        self.clc += 1
        # print 'Decode edge'
        dfMap.xs(1)[self.clc] = activeList.map.toString()
        dfMap.xs(2)[self.clc] = activeList.ROBToString()
        dfMap.xs(3)[self.clc] = activeList.busy_bit_tables.to_string()
        dfMap.xs(4)[self.clc] = activeList.map.Note
        dfMap.xs(5)[self.clc] = activeList.integer_queue.to_string()
        dfMap.xs(6)[self.clc] = activeList.fp_queue.to_string()

        if self.currIssuedInstrs:
            for k in sorted(self.currIssuedInstrs.keys()):
                # print 'assigning this:',self.currInstrs[k] ,'sth', self.currDecodedInstrs[k]
                # df.xs(k)['Instruction'] = ''+self.currInstrs[k] +' # Decoded: '+ self.currDecodedInstrs[k]
                df.xs(k)['Logical'] = self.currDecodedInstrs[k].toStr()
                df.xs(k)['Physical'] = self.currDecodedInstrs[k].toMappedStr(activeList.map.LogToPhy)
                
                print k, self.clc
                df.xs(k)[str(self.clc)] = 'ID'
                # print 'registered an ID stage on location:', k, self.clc

            # empty the "queue"
            # self.currInstrs = None
            
            # dfMap.xs(0)[self.clc] = activeList.map.prettyTable()
        

