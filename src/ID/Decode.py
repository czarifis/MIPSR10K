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
        self.i = 0
        self.currInstrs = None
        self.clc = 0
        self.currDecodedInstrs = {}

    

    def calc(self,df,instructions,activeList):
        # print 'Decode calc'
       
        if instructions is not None:
            # print instructions
            # Inst = ins.Instruction()
            
            self.currInstrs = instructions
            self.iterOverInstructions(activeList)
        
    # This function iterates over 4 instructions at each cycle
    def iterOverInstructions(self,activeList):
        for instr in self.currInstrs:
            actualInstr = self.currInstrs[instr]
            print 'Instruction about to get decoded:',actualInstr
            Inst = ins.Instruction(actualInstr)
            Inst.printInstr()
            self.currDecodedInstrs[instr] = Inst
            activeList.process(Inst)
       
            

    def edge(self,df,dfMap,activeList):
        self.clc+=1
        # print 'Decode edge'
        dfMap.xs(1)[self.clc] = activeList.map.toString()
        dfMap.xs(2)[self.clc] = activeList.map.Note


            

        if self.currInstrs is not None:
            for k in self.currInstrs.keys():
                # print 'assigning this:',self.currInstrs[k] ,'sth', self.currDecodedInstrs[k]
                # df.xs(k)['Instruction'] = ''+self.currInstrs[k] +' # Decoded: '+ self.currDecodedInstrs[k]
                df.xs(k)['Logical'] = self.currDecodedInstrs[k].toStr()
                df.xs(k)['Physical'] = self.currDecodedInstrs[k].toMappedStr(activeList.map.LogToPhy)
                
                
                print k,self.clc
                df.xs(k)[self.clc] = 'ID'

            # empty the "queue"
            self.currInstrs = None
            
            # dfMap.xs(0)[self.clc] = activeList.map.prettyTable()
        
       
        


    def readInsts(self):
        pass
