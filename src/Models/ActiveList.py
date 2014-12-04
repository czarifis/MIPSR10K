import FreeList
import RegisterMapTables

class ActiveListRecord:
    '''
        Each record in the Active List contains:
         * the logical DESTINATION register
         * the physical register
    '''
    def __init__(self,logical,physical):
        self.logicalDest = logical
        self.physical = physical

class ActiveList:
    
    '''
        ROB
         * It has to remove instructions when they commit
         * It has to remove instructions if a mispredicted 
         * branch or an exception causes them to abort
    '''
    def __init__(self):
        self.ROB = {}
        self.curr = 0

        ### Extra stuff that I don't know where to put ###
        self.freeList = FreeList.FreeList()
        self.map = RegisterMapTables.RegisterMapTables()

        # There are 32 addresses in the ActiveList 
        for i in range(32):
            self.ROB[i] = None

    def process(self,instr):
        if instr.op == 'L':
            # print instr.rt,'<-',instr.extra,'(',instr.rs,')'
            pass
        elif instr.op == 'S':
            # print instr.rt,'->',instr.extra,'(',instr.rs,')'
            pass
        elif instr.op == 'I':
            # print instr.rd,'<-',instr.rs,'INTOP',instr.rt
            prd = self.freeList.assign()
            prs = self.freeList.assign()
            prt = self.freeList.assign()

            if prd == None or prs == None or prt == None:
                raise Exception("Free List is Empty!")
            else:
                print 'will map the following:'
                print instr.rd,'->',prd
                self.map.setLog2Phy(instr.rd,prd)
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)

        elif instr.op == 'A':
            # print instr.rd,'<-',instr.rs,'FPADD',instr.rt
            pass
        elif instr.op == 'M':
            # print instr.rd,'<-',instr.rs,'FPMUL',instr.rt
            pass
        elif instr.op == 'B':
            # print 'BEQ,',instr.rs,',',instr.rt,',xx,',instr.prediction
            pass

