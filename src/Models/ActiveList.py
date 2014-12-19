'''
Created on Dec 2, 2014

@author: Costas Zarifis
'''
import FreeList
import RegisterMapTables
import busyBitTables
import IntegerQueue
import AddressQueue
import FPQueue
import copy
import BranchStack


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
        self.inst_graduated = None

    def to_string(self):
        if self.instruction is None:
            return 'None'
        else:
            return str((self.logicalDest, self.physical, self.done, self.graduated, self.instruction.line_number))

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
        self.inst_graduated_previously = None
        self.line_graduated_previously = -1
        # self.ROB = {}
        self.curr_length = 0
        self.branch_happened = False
        self.branch_info = None

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

        # Address Queue
        self.address_queue = AddressQueue.AddressQueue()

        # Branch Stack
        self.branch_stack = BranchStack.BranchStack()

        # There are 32 addresses in the ActiveList 
        for i in range(32):
            self.ROB.append(ActiveListRecord(None, None, None))
        #     self.ROB[i] =

    # This function adds a record at the branch stack
    def add2Branch_stack(self, rob):
        self.branch_stack.add2stack(rob)

    def return_instructions_after_branch(self, branch):
        ret = {}
        counter = 0
        remove_from_rob = []
        self.branch_happened = True
        self.branch_info = branch
        for e in self.ROB:
            if e.instruction is not None:
                if branch.line_number <= e.instruction.line_number:
                    # Counter used to shift instructions
                    counter += 1
                    self.busy_bit_tables.setAsNonBusy(e.instruction.prd)
                    self.freeList.freeReg(e.instruction.prd)
                    self.map.remove_logical(e.instruction.prd)
                    e.graduated = True
                    e.done = True
                    e.logicalDest = None
                    # e.instruction = None
                    e.physical = None
                    # remove_from_rob.append(e)



        for e in self.ROB:
            if e.instruction is not None:
                if branch.line_number == e.instruction.line_number:
                    print 'found branch!!'
                    branch_str = e.instruction.initial_instr
                    branch_str = branch_str[:-1]
                    branch_str += '0'
                    ret[e.instruction.line_number+counter] = (e.instruction.line_number+counter, branch_str)
                if branch.line_number < e.instruction.line_number:
                    ret[e.instruction.line_number+counter] = (e.instruction.line_number+counter, e.instruction.initial_instr)

        # for el in remove_from_rob:
        #     self.ROB.remove(el)
        # self.ROB = branch.ROB
        return ret

    # This func adds a tuple into the ROB
    def add2ROB(self, line, logical, physical, inst):
        line -= 1

        instruction_record = self.ROB[line % 32]
        if instruction_record.graduated is False:
            # hmm apparently the instruction is still executing
            raise 'ROB is full!'
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

    def check_if_prev_graduated(self, line):
        for e in self.ROB:
            if e.instruction is not None:
                if line > e.instruction.line_number:
                    if e.graduated is False:
                        return False
        return True

    def pop_from_active_list(self):
        ret_list = []
        counter = 0
        rem_counter = 0
        prev_element = None

        # if self.inst_graduated_previously is None:
        #     for e in self.ROB:
        #         if e.done_but_not_graduated() is True:
        #


        for e in self.ROB:

            if e.done_but_not_graduated() is True:
                if self.inst_graduated_previously is None:
                    if e.instruction.line_number != 2:
                        e.graduated = True
                        ret_list.append(e.instruction)
                        self.inst_graduated_previously = e.instruction
                        self.line_graduated_previously = rem_counter
                        counter += 1
                        if counter % 4 == 0:
                            break

                else:
                    if self.branch_happened:
                        if e.instruction.line_number > self.branch_info.line_number:
                            if self.check_if_prev_graduated(e.instruction.line_number):
                                self.branch_happened = False
                                e.graduated = True
                                ret_list.append(e.instruction)
                                self.inst_graduated_previously = e.instruction
                                self.line_graduated_previously = rem_counter
                                counter += 1
                                if counter % 4 == 0:
                                    break
                                print 'Boom'
                                pass
                        else:
                            ll1 = self.line_graduated_previously + 1
                            ll = ll1 % 32
                            if ll == rem_counter:
                                e.graduated = True
                                ret_list.append(e.instruction)
                                self.inst_graduated_previously = e.instruction
                                self.line_graduated_previously = rem_counter
                                counter += 1
                                if counter % 4 == 0:
                                    break
                                pass
                    else:
                        ll1 = self.line_graduated_previously + 1
                        ll = ll1 % 32
                        if ll == rem_counter:
                            e.graduated = True
                            ret_list.append(e.instruction)
                            self.inst_graduated_previously = e.instruction
                            self.line_graduated_previously = rem_counter
                            counter += 1
                            if counter % 4 == 0:
                                break
                            pass
            rem_counter += 1
                # else:


        # for e in self.ROB:
        #
        #     if e.done_but_not_graduated() is True:
        #
        #         if prev_element is None:
        #             prev_element2 = self.ROB[len(self.ROB)-1]
        #             if prev_element2.graduated:
        #                 e.graduated = True
        #                 ret_list.append(e.instruction)
        #                 self.inst_graduated_previously = e.instruction
        #                 counter += 1
        #                 if counter % 4 == 0:
        #                     break
        #         elif prev_element.graduated:
        #             e.graduated = True
        #             ret_list.append(e.instruction)
        #             self.inst_graduated_previously = e.instruction
        #             counter += 1
        #             if counter % 4 == 0:
        #                 break
        #         else:
        #             break
        #     prev_element = e
        return ret_list

    # This function gets called when there's a mispredict
    # and the instructions following the branch are supposed
    # to get issued.
    def issue_mispredict(self, data):
        self.fp_queue.mispredict_clear(data)





    # This function returns a string representation of the ROB
    def ROBToString(self):
        ret = ''
        for i in range(32):
            ret += str(i+1)+'-'+(self.ROB[i]).to_string()+' '
        return ret


    def fp_queue_pop(self, operation):
        return self.fp_queue.pop(operation)

    def int_queue_pop(self, operation):
        return self.integer_queue.pop(operation)

    def address_queue_pop(self):
        return self.address_queue.pop()

    def address_queue_pop2execute(self):
        return self.address_queue.in_order_pop()

    def address_queue_address_of_line_is_ready(self, inst):
        self.address_queue.set_address_as_computed(inst)

    # This process is used during the decoding stage to take care
    # of all the Queues :)
    def process_add2queue(self, instr):
        if instr.op == 'L':
            self.address_queue.add2queue(self.busy_bit_tables, self.map, instr)
            pass
        elif instr.op == 'S':
            self.address_queue.add2queue(self.busy_bit_tables, self.map, instr)
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


    # This function is used by the Issue stage to go over all the instructions that
    # Are still in the queues
    def go_over_queues(self):
        ret = []
        ret = ret + self.integer_queue.return_instructions()
        ret = ret + self.fp_queue.return_instructions()
        ret = ret + self.address_queue.return_instructions()
        return ret

    # This process is used during the decoding stage to take care
    # Free Lists, busy bit tables, register map tables, instruction
    # object generation and pretty much everything other than the
    # Queues :)
    def process_decode(self, line, instr):

        if instr.op == 'L':
            # print instr.rt, '<-', instr.extra, '(', instr.rs, ')'

            # r0 is always I0
            if instr.rs == 'r0':
                prs = 'I0'
            else:
                # If this happens there's a hazard RAW or RAR
                prs = self.map.isMapped(instr.rs)
                if prs is None:
                    prs = self.freeList.assign()
            self.map.setLog2Phy(instr.rs, prs)

            # prs = self.freeList.assign()
            # This is the destination

            if instr.rt is 'r0':
                prt = 'I0'
            else:
                # prt = self.map.isMapped(instr.rt)
                # if prt is None:
                prt = self.freeList.assign()

            self.map.setLog2Phy(instr.rt, prt)
            if prs is None or prt is None:
                self.map.setNote('We are out of Physical Registers')

            else:
                print 'will map the following:'
                print instr.rs, '->', prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt, '->', prt
                self.map.setLog2Phy(instr.rt,prt)

                instr.prs = prs
                instr.prt = prt
                
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
            if instr.rs == 'r0':
                prs = 'I0'
            else:
                prs = self.map.isMapped(instr.rs)
                if prs == None:
                    prs = self.freeList.assign()
            self.map.setLog2Phy(instr.rs,prs)

            if instr.rt == 'r0':
                prt = 'I0'
            else:
                prt = self.map.isMapped(instr.rt)
                if prt == None:
                    prt = self.freeList.assign()
            self.map.setLog2Phy(instr.rt,prt)
            
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

                instr.prs = prs
                instr.prt = prt

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

            if instr.rs == 'r0':
                prs = 'I0'
            else:
                prs = self.map.isMapped(instr.rs)
                if prs is None:
                    prs = self.freeList.assign()
            self.map.setLog2Phy(instr.rs,prs)

            if instr.rt == 'r0':
                prt = 'I0'
            else:
                prt = self.map.isMapped(instr.rt)
                if prt is None:
                    prt = self.freeList.assign()
            self.map.setLog2Phy(instr.rt,prt)

            if instr.rd == 'r0':
                prd = 'I0'
            else:
                prd = self.freeList.assign()
            self.map.setLog2Phy(instr.rd,prd)
            # prs = self.freeList.assign()
            # prt = self.freeList.assign()

            if prd is None or prs is None or prt is None:
                self.map.setNote('We are out of Physical Registers')
            else:
                print 'will map the following:'
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)
                print instr.rd,'->',prd
                self.map.setLog2Phy(instr.rd,prd)


                instr.prs = prs
                instr.prt = prt
                instr.prd = prd
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

            if instr.rs == 'r0':
                prs = 'I0'
            else:
                prs = self.map.isMapped(instr.rs)
                if prs is None:
                    prs = self.freeList.assign()
            self.map.setLog2Phy(instr.rs,prs)

            if instr.rt == 'r0':
                prt = 'I0'
            else:
                prt = self.map.isMapped(instr.rt)
                if prt is None:
                    prt = self.freeList.assign()
            self.map.setLog2Phy(instr.rt,prt)

            if instr.rd == 'r0':
                prd = 'I0'
            else:
                prd = self.freeList.assign()
            self.map.setLog2Phy(instr.rd,prd)
            # prs = self.freeList.assign()
            # prt = self.freeList.assign()

            if prd == None or prs == None or prt == None:
                self.map.setNote('We are out of Physical Registers')
            else:
                print 'will map the following:'
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)
                print instr.rd,'->',prd
                self.map.setLog2Phy(instr.rd,prd)


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

            pass
        elif instr.op == 'M':
            # print instr.rd,'<-',instr.rs,'FPMUL',instr.rt
            # print instr.rd,'<-',instr.rs,'INTOP',instr.rt

            if instr.rs == 'r0':
                prs = 'I0'
            else:

                prs = self.map.isMapped(instr.rs)
                if prs == None:
                    prs = self.freeList.assign()
            self.map.setLog2Phy(instr.rs,prs)

            if instr.rt == 'r0':
                prt = 'I0'
            else:
                prt = self.map.isMapped(instr.rt)
                if prt == None:
                    prt = self.freeList.assign()

            self.map.setLog2Phy(instr.rt,prt)
            
            if instr.rd == 'r0':
                prd = 'I0'
            else:
                prd = self.freeList.assign()
            self.map.setLog2Phy(instr.rd,prd)
            # prs = self.freeList.assign()
            # prt = self.freeList.assign()

            if prd == None or prs == None or prt == None:
                self.map.setNote('We are out of Physical Registers')
            else:
                print 'will map the following:'
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)
                print instr.rd,'->',prd
                self.map.setLog2Phy(instr.rd,prd)

                mappedInstr = prd,'<-',prs,'FPMUL',prt

                instr.prs = prs
                instr.prt = prt
                instr.prd = prd
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

            if instr.rs == 'r0':
                prs = 'I0'
            else:
                prs = self.map.isMapped(instr.rs)
                if prs is None:
                    prs = self.freeList.assign()
            self.map.setLog2Phy(instr.rs, prs)

            if instr.rt == 'r0':
                prt = 'I0'
            else:
                prt = self.map.isMapped(instr.rt)
                if prt is None:
                    prt = self.freeList.assign()
            self.map.setLog2Phy(instr.rt,prt)

            # prs = self.freeList.assign()
            # prt = self.freeList.assign()

            if prs is None or prt is None:
                self.map.setNote('We are out of Physical Registers')

            else:
                print 'will map the following:'
                print instr.rs,'->',prs
                self.map.setLog2Phy(instr.rs,prs)
                print instr.rt,'->',prt
                self.map.setLog2Phy(instr.rt,prt)
                mappedInstr = 'BEQ,',prs,',',prt,',xx,',instr.prediction
                instr.prs = prs
                instr.prt = prt

                instr.ROB = copy.deepcopy(self.ROB)



                instr.add2MappedDecoding(mappedInstr)

                self.add2ROB(line, instr.rt, prt, instr)


            # pass



