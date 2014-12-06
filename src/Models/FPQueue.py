'''
Created on Dec 5, 2014

@author: Costas Zarifis
'''

from collections import defaultdict


class FPQueueRecord:
    def __init__(self, i1, i2, busy_bit_t, instr):
        self.I1 = i1
        self.I1Busy = busy_bit_t.isBusy(i1)
        self.I2 = i2
        self.I2Busy = busy_bit_t.isBusy(i2)
        self.Instruction = instr


    def to_string(self):
        ret = ''
        ret += '('+str(self.I1)+','+str(self.I1Busy)+')'
        ret += '('+str(self.I2)+','+str(self.I2Busy)+')'
        return ret

    def is_busy(self):
        if self.I1Busy or self.I2Busy:
            return True
        else:
            return False

    # This function gets a physical register and
    # makes it available inside the queue
    def make_available(self, reg):
        if self.I1 == reg:
            self.I1Busy = False
        if self.I2 == reg:
            self.I2Busy = False


class FPQueue:
    def __init__(self):
        self.queue = defaultdict(list)
        self.queue['FPADD'] = []
        self.queue['FPMUL'] = []
        # self.queue['ALU1']
        self.current_size = 0
        self.MAX_SIZE = 16

    # Adding instruction to FP Queue
    def add2queue(self, tp, busy_bit_table, register_map, instruction):
        print '#### FP Queue ####'
        if tp is 'FPADD' or tp is 'FPMUL':
            self.current_size += 1

            # Checking if there's enough space in the queue for a new instruction
            if self.current_size == self.MAX_SIZE:
                self.current_size -= 1
                # I guess an exception is fine for now...
                raise Exception('FP Queue can only hold'
                                ' up to 16 instructions')
            else:

                print 'rt:', instruction.rt, instruction.prt
                print 'rs:', instruction.rs, instruction.prs

                # Adding the current instruction to the Integer Queue
                rec = FPQueueRecord(instruction.prt,
                                    instruction.prs,
                                    busy_bit_table, instruction)
                self.queue[tp].append(rec)
        else:
            raise Exception('FP Queue can only hold'
                            ' instructions that intend to '
                            'go to either ALU1 or ALU2')

    # This instruction returns a none busy record from the queue
    def pop(self, op):
        if not self.queue[op]:
            # No elements exist in the corresponding queue
            return None
        else:
            # OK! Let's traverse the queue to find if there
            # are any ready to go (non-busy) tuples
            for element in self.queue[op]:
                if element.is_busy() is False:
                    self.queue[op].remove(element)
                    return element
            return None

        # return None

    def make_available(self, op, register):
        if not self.queue[op]:
            # No elements exist in the corresponding queue
            return None
        else:
            # OK! Let's traverse the queue to find if there
            # registers that should be available on the next cycle
            for element in self.queue[op]:
                element.make_available(register)



    def to_string(self):
        if self.current_size == 0:
            return 'empty!'
        ret = ''
        for k in self.queue.keys():
            ret += str(k)+':[ '
            for e in self.queue[k]:
                ret += e.to_string()+' '
            ret += ']'

        return ret


