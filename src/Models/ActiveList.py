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
        self.busy = False

class ActiveList:
    
    '''
        ROB
         * It has to remove instructions when they commit
         * It has to remove instructions if a mispredicted 
         * branch or an exception causes them to abort
    '''
    def __init__(self):
        self.ROB = []
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

            # If this happens there's a hazard RAW or RAR
            prs = self.map.isMapped(instr.rs)
            if prs == None:
                prs = self.freeList.assign()
            else:
                print 'potential hazard'
            # prs = self.freeList.assign()
            # This is the destination
            prt = self.freeList.assign()
            if prs == None or prt == None:
                self.map.setNote('We are out of Physical Registers')
                # class providing printing functionalitu
                pm = pr.prettifyme()
                
                pm.printme(df,dfMap, args.output)
            else:
                print 'will map the following:'
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)
                
                mappedInstr = prt,'<-',instr.extra,'(',prs,')'
                instr.add2MappedDecoding(mappedInstr)
            pass
        elif instr.op == 'S':
            # print instr.rt,'->',instr.extra,'(',instr.rs,')'
            # prd = self.
            # If this happens there's a hazard RAW or RAR
            prs = self.map.isMapped(instr.rs)
            if prs == None:
                prs = self.freeList.assign()
            
            prt = self.map.isMapped(instr.rt)
            if prt == None:
                prt = self.freeList.assign()
            
            # prs = self.freeList.assign()
            # prt = self.freeList.assign()
            if prs == None or prt == None:
                self.map.setNote('We are out of Physical Registers')
            else:
                print 'will map the following:'
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)

                mappedInstr = prt,'->',instr.extra,'(',prs,')'
                instr.add2MappedDecoding(mappedInstr)

        elif instr.op == 'I':
            # print instr.rd,'<-',instr.rs,'INTOP',instr.rt

            prs = self.map.isMapped(instr.rs)
            if prs == None:
                prs = self.freeList.assign()
            
            prt = self.map.isMapped(instr.rt)
            if prt == None:
                prt = self.freeList.assign()
            


            prd = self.freeList.assign()
            # prs = self.freeList.assign()
            # prt = self.freeList.assign()

            if prd == None or prs == None or prt == None:
                self.map.setNote('We are out of Physical Registers')
            else:
                print 'will map the following:'
                print instr.rd,'->',prd
                self.map.setLog2Phy(instr.rd,prd)
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)
                mappedInstr = prd,'<-',prs,'INTOP',prt
                instr.add2MappedDecoding(mappedInstr)

            # if prd == None or prs == None or prt == None:
            #     self.map.setLog2Phy('Note','We are out of Physical Registers')
            # else:
            #     print 'will map the following:'
            #     print instr.rd,'->',prd
            #     self.map.setLog2Phy(instr.rd,prd)
            #     print instr.rs,'->',prs
            #     self.map.setLog2Phy(instr.rs,prs)
            #     print instr.rt,'->',prt
            #     self.map.setLog2Phy(instr.rt,prt)

        elif instr.op == 'A':
            # print instr.rd,'<-',instr.rs,'FPADD',instr.rt
            # print instr.rd,'<-',instr.rs,'INTOP',instr.rt

            prs = self.map.isMapped(instr.rs)
            if prs == None:
                prs = self.freeList.assign()
            
            prt = self.map.isMapped(instr.rt)
            if prt == None:
                prt = self.freeList.assign()
            

            prd = self.freeList.assign()
            # prs = self.freeList.assign()
            # prt = self.freeList.assign()

            if prd == None or prs == None or prt == None:
                self.map.setNote('We are out of Physical Registers')
            else:
                print 'will map the following:'
                print instr.rd,'->',prd
                self.map.setLog2Phy(instr.rd,prd)
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)

                mappedInstr = prd,'<-',prs,'FPADD',prt
                instr.add2MappedDecoding(mappedInstr)

            # pass
        elif instr.op == 'M':
            # print instr.rd,'<-',instr.rs,'FPMUL',instr.rt
            # print instr.rd,'<-',instr.rs,'INTOP',instr.rt

            prs = self.map.isMapped(instr.rs)
            if prs == None:
                prs = self.freeList.assign()
            
            prt = self.map.isMapped(instr.rt)
            if prt == None:
                prt = self.freeList.assign()
            

            prd = self.freeList.assign()
            # prs = self.freeList.assign()
            # prt = self.freeList.assign()

            if prd == None or prs == None or prt == None:
                self.map.setNote('We are out of Physical Registers')
            else:
                print 'will map the following:'
                print instr.rd,'->',prd
                self.map.setLog2Phy(instr.rd,prd)
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)

                mappedInstr = prd,'<-',prs,'FPMUL',prt
                instr.add2MappedDecoding(mappedInstr)
            # pass
        elif instr.op == 'B':
            # print 'BEQ,',instr.rs,',',instr.rt,',xx,',instr.prediction
            # print instr.rd,'<-',instr.rs,'INTOP',instr.rt
            # prd = self.freeList.assign()

            prs = self.map.isMapped(instr.rs)
            if prs == None:
                prs = self.freeList.assign()
            
            prt = self.map.isMapped(instr.rt)
            if prt == None:
                prt = self.freeList.assign()
            

            # prs = self.freeList.assign()
            # prt = self.freeList.assign()

            if prs == None or prt == None:
                self.map.setNote('We are out of Physical Registers')

            else:
                print 'will map the following:'
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)
                mappedInstr = 'BEQ,',prs,',',prt,',xx,',instr.prediction
                instr.add2MappedDecoding(mappedInstr)
            # pass

