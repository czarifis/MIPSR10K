'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''


'''
This class provides all the functionality for decoding instructions
'''
import Models.Instruction as ins

class Decode:

    def __init__(self):
        self.i = 0
        self.currInstrs = None
        self.clc = 0

    

    def calc(self,df,instructions):
        # print 'Decode calc'
        if instructions is not None:
            # print instructions
            # Inst = ins.Instruction()
            
            self.currInstrs = instructions
            self.iterOverInstructions()
        
        
    def iterOverInstructions(self):
        for instr in self.currInstrs:
            actualInstr = self.currInstrs[instr]
            print 'Instruction about to get decoded:',actualInstr
            Inst = ins.Instruction(actualInstr)
            Inst.printInstr()
       
            

    def edge(self,df):
        self.clc+=1
        # print 'Decode edge'

        if self.currInstrs is not None:
            for k in self.currInstrs.keys():
                
                # print k,self.clc
                df.xs(k)[self.clc] = 'ID'

            # empty the "queue"
            self.currInstrs = None
       
        


    def readInsts(self):
        pass
