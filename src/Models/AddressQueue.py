'''
Created on Dec 15, 2014

@author: Costas Zarifis
'''

from collections import defaultdict

# Class that describes a record inside the integer queue


class AddressQueueRecord:
    def __init__(self, i1, i2, address, address_busy, busy_bit_t, instr):
        self.I1 = i1
        if i1 == 'I0':
            self.I1Busy = False
        else:
            self.I1Busy = busy_bit_t.isBusy(i1)
        self.I2 = i2
        if i2 == 'I0':
            self.I2Busy = False
        else:
            self.I2Busy = busy_bit_t.isBusy(i2)
        self.Address = address
        self.Address_busy = address_busy
        self.Address_computed = False
        self.issued = False

        self.Instruction = instr

    # to_string method used to "pretty print" the output into a matrix
    def to_string(self):
        ret = ''
        ret += '('+str(self.I1)+','+str(self.I1Busy)+')'
        ret += '('+str(self.I2)+','+str(self.I2Busy)+')'
        ret += '('+str(self.Address)+','+str(self.Address_busy)+')'
        ret += '(Address computed:'+str(self.Address_computed)+')}'
        return ret

    # checks if the current record is busy
    def is_busy(self):
        if self.I1Busy or self.I2Busy or self.Address_busy:
            return True
        else:
            return False
            # if self.Address_computed is False:
            #     return False
            # else:
            #     return True

    # This function gets a physical register and
    # makes it available inside the queue
    def make_available(self, reg):
        if self.I1 == reg:
            self.I1Busy = False
        if self.I2 == reg:
            self.I2Busy = False

    # Same as before but for addresses.
    def make_address_available(self, addr):
        if self.Address == addr:
            self.Address_busy = False


# Class describing the Integer Queue


class AddressQueue:
    def __init__(self):

        self.queue = []
        # self.queue['ALU1'] = []
        # self.queue['ALU2'] = []
        # self.queue['ALU1']
        self.current_size = 0
        self.MAX_SIZE = 16

    # Adding instruction to integer Queue
    def add2queue(self, busy_bit_table, register_map, instruction):
        print '#### Address Queue ####'
        # if tp is 'L' or tp is 'S':
        self.current_size += 1
        # Checking if there's enough space in the queue for a new instruction
        if self.current_size > self.MAX_SIZE:
            self.current_size -= 1
            # I guess an exception is fine for now...
            raise Exception('Address Queue can only hold'
                            ' up to 16 instructions')
        else:
            # print 'rt:', instruction.rt, instruction.prt
            print 'rs:', instruction.rs, instruction.prs

            # Adding the current instruction to the Integer Queue

            ###############################################################
            # will need to change that to figure out address dependencies #
            ###############################################################
            # (self, i1, i2, address, address_busy, busy_bit_t, instr):
            rec = AddressQueueRecord(instruction.prs,instruction.prt, instruction.extra, False, busy_bit_table, instruction)
            print rec
            self.queue.append(rec)

    # else:
    #         raise Exception('Address Queue can only hold'
    #                         ' instructions that are either'
    #                         ' store or load')

    # This instruction returns a non-busy record from the queue
    def pop(self):
        if not self.queue:
            # No elements exist in the corresponding queue
            return None
        else:
            # OK! Let's traverse the queue to find if there
            # are any ready to go (non-busy) tuples
            for element in self.queue:
                if (element.is_busy() is False) and (element.issued is False):
                    # self.queue.remove(element)
                    # self.current_size -= 1
                    element.issued = True
                    return element
            return None

    # This function is used by the LS execution unit to pop instructions in order
    def in_order_pop(self):
        if not self.queue:
            # No elements exist in the corresponding queue
            return None
        else:
            e = self.queue[0]
            if e.is_busy() is False and e.Address_computed is True:
                print e, 'is ready to LS'
                self.queue.remove(e)
                self.current_size -= 1
                return e

    # This function returns every instruction that is still inside the integer queue
    def return_instructions(self):
        ret = []
        addr_list = self.queue
        for e in addr_list:
            if e.issued is False:
                ret.append(e.Instruction)
        return ret

    # This function set's the address of the corresponding element
    # to computed when the final address is ready (after the first
    # stage of the LS)
    def set_address_as_computed(self, instr):
        for e in self.queue:
            if e.Instruction.line_number == instr.line_number:
                e.Address_computed = True
                break


    # This function switches a busy element of a queue into a non-busy one
    # Used mainly to forward values that have finished executing but are not
    # graduated yet

    def make_available(self, register):
        if not self.queue:
            # No elements exist in the corresponding queue
            return None
        else:
            # OK! Let's traverse the queue to find if there
            # registers that should be available on the next cycle
            for element in self.queue:
                element.make_available(register)

    # function used for "pretty printing"
    def to_string(self):
        if self.current_size == 0:
            return 'empty!'
        ret = ''
        ret += '[ '
        for e in self.queue:
            ret += e.to_string()+' '
        ret += ']'

        return ret


