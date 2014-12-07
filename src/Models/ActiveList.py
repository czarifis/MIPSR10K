'''
Created on Dec 2, 2014

@author: Costas Zarifis
'''
import FreeList
import RegisterMapTables
import busyBitTables
import IntegerQueue
import FPQueue


class ActiveListRecord:

    '''
        Each record in the Active List contains:
         * the logical DESTINATION register
         * the physical register
         * a bit specifying if the current  
    '''
    def __init__(self, logical, physical, instr):
        self.logicalDest = logical
        self.physical = physical
        self.done = True
        self.graduated = True
        self.instruction = instr

    def to_string(self):
        return str((self.logicalDest, self.physical, self.done))

    def set2done(self):
        self.done = True

    # returns True if the instruction is done but not graduated
    # False in all other cases...
    def done_but_not_graduated(self):
        if self.done is True and self.graduated is False:
            return True
        else:
            return False


class ActiveList:
    
    '''
        ROB
         * 32 Instructions can be active so it should be having 32 spots
         * It has to remove instructions when they commit
         * It has to remove instructions if a mispredicted 
         * branch or an exception causes them to abort
    '''
    def __init__(self):
        self.ROB = []
        # self.ROB = {}
        self.curr_length = 0

        ### Extra stuff that I don't know where to put ###

        # Free List of physical registers
        self.freeList = FreeList.FreeList()

        # Mappings of logical to physical registers
        self.map = RegisterMapTables.RegisterMapTables()

        # Lookup table that keeps the information of whether or not
        # a physical register is busy or not
        self.busy_bit_tables = busyBitTables.busyBitTables()

        # Integer Queue
        self.integer_queue = IntegerQueue.IntegerQueue()

        # FP Queue
        self.fp_queue = FPQueue.FPQueue()

        # There are 32 addresses in the ActiveList 
        for i in range(32):
            self.ROB.append(ActiveListRecord(None, None, None))
        #     self.ROB[i] =

    # This func adds a tuple into the ROB
    def add2ROB(self, line, logical, physical, inst):
        line -= 1
        instruction_record = self.ROB[line % 32]
        if instruction_record.done is False:
            # hmm apparently the instruction is still executing
            return False
        else:
            new_record = ActiveListRecord(logical, physical, inst)
            new_record.done = False
            new_record.graduated = False

            self.ROB[line % 32] = new_record
            return True
        # if self.curr_length < 32:
        #     self.ROB.append(ActiveListRecord(logical, physical))
        #     self.curr_length += 1
        # else:
        #     print 'Active List is full!'

    # When an instruction gets executed we have to update the corresponding done bi
    def set_rob_record2done(self, line):
        self.ROB[(line-1) % 32].set2done()

    def pop_from_active_list(self):
        ret_list = []
        counter = 0
        for e in self.ROB:
            counter += 1
            if e.done_but_not_graduated() is True:
                e.graduated = True
                ret_list.append(e.instruction)
                if counter % 4 == 0:
                    break
        return ret_list



    # This function returns a string representation of the ROB
    def ROBToString(self):
        ret = ''
        for i in range(32):
            ret += str(i+1)+'-'+(self.ROB[i]).to_string()+' '
        return ret


    def fp_queue_pop(self, operation):
        return self.fp_queue.pop(operation)

    # This process is used during the decoding stage to take care
    # of all the Queues :)
    def process_issue(self, instr):
        if instr.op == 'L':
            pass
        elif instr.op == 'S':
            pass
        elif instr.op == 'I':
            # Adding instruction to integer queue
            self.integer_queue.add2queue('ALU2', self.busy_bit_tables, self.map, instr)

        elif instr.op == 'A':
            # Adding instruction to fp queue
            self.fp_queue.add2queue('FPADD', self.busy_bit_tables, self.map, instr)

        elif instr.op == 'M':
            # Adding instruction to fp queue
            self.fp_queue.add2queue('FPMUL', self.busy_bit_tables, self.map, instr)

        elif instr.op == 'B':
            # Adding instruction to integer queue
            self.integer_queue.add2queue('ALU1', self.busy_bit_tables, self.map, instr)


    # This process is used during the decoding stage to take care
    # Free Lists, busy bit tables, register map tables, instruction
    # object generation and pretty much everything other than the
    # Queues :)
    def process_decode(self, line, instr):

        if instr.op == 'L':
            # print instr.rt,'<-',instr.extra,'(',instr.rs,')'

            # If this happens there's a hazard RAW or RAR
            prs = self.map.isMapped(instr.rs)
            if prs is None:
                prs = self.freeList.assign()

            # prs = self.freeList.assign()
            # This is the destination
            prt = self.freeList.assign()
            if prs is None or prt is None:
                self.map.setNote('We are out of Physical Registers')

            else:
                print 'will map the following:'
                print instr.rs, '->', prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt, '->', prt
                self.map.setLog2Phy(instr.rt,prt)
                
                mappedInstr = prt, '<-', instr.extra, '(', prs, ')'
                instr.add2MappedDecoding(mappedInstr)

                # Will set the physical register used as a destination to busy
                self.busy_bit_tables.setAsBusy(prt)

                # Adding that to ROB
                self.add2ROB(line, instr.rt, prt, instr)
            # pass
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

                # Will set the physical register used as a destination to busy
                # Nope! There is no actual destination register here
                # self.busy_bit_tables.setAsBusy(prt)

                # There is no destination register for store words what do I do as far as ROB goes?
                # Oh Well let's insert it for now
                self.add2ROB(line, instr.rt, prt, instr)
        elif instr.op == 'I':
            # print instr.rd,'<-',instr.rs,'INTOP',instr.rt

            prs = self.map.isMapped(instr.rs)
            if prs is None:
                prs = self.freeList.assign()
            
            prt = self.map.isMapped(instr.rt)
            if prt is None:
                prt = self.freeList.assign()
            


            prd = self.freeList.assign()
            # prs = self.freeList.assign()
            # prt = self.freeList.assign()

            if prd is None or prs is None or prt is None:
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

                # Will set the physical register used as a destination to busy
                self.busy_bit_tables.setAsBusy(prd)

                # # Adding instruction to integer queue
                # self.integer_queue.add2queue('ALU2', self.busy_bit_tables, self.map, instr)
                # Adding that to ROB
                self.add2ROB(line, instr.rd, prd, instr)

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

                instr.prs = prs
                instr.prt = prt
                instr.prd = prd
                mappedInstr = prd,'<-',prs,'FPADD',prt
                instr.add2MappedDecoding(mappedInstr)

                # Will set the physical register used as a destination to busy
                self.busy_bit_tables.setAsBusy(prd)

                # Adding instruction to fp queue
                # self.fp_queue.add2queue('FPADD', self.busy_bit_tables, self.map, instr)

                # Adding that to ROB
                self.add2ROB(line, instr.rd, prd, instr)

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

                # Will set the physical register used as a destination to busy
                self.busy_bit_tables.setAsBusy(prd)

                # Adding instruction to fp queue
                # self.fp_queue.add2queue('FPMUL', self.busy_bit_tables, self.map, instr)

                # Adding that to ROB
                self.add2ROB(line, instr.rd, prd, instr)
            # pass
        elif instr.op == 'B':
            # print 'BEQ,',instr.rs,',',instr.rt,',xx,',instr.prediction
            # print instr.rd,'<-',instr.rs,'INTOP',instr.rt
            # prd = self.freeList.assign()

            prs = self.map.isMapped(instr.rs)
            if prs is None:
                prs = self.freeList.assign()
            
            prt = self.map.isMapped(instr.rt)
            if prt is None:
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

                # self.integer_queue.add2queue('ALU1', self.busy_bit_tables, self.map, instr)

                # Should I add sth to ROB?

            # pass

