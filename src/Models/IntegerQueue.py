'''
Created on Dec 5, 2014

@author: Costas Zarifis
'''

from collections import defaultdict


class IntegerQueueRecord:
    def __init__(self, i1, i2, busy_bit_t, instr):
        self.I1 = (i1, busy_bit_t.isBusy(i1))
        self.I2 = (i2, busy_bit_t.isBusy(i2))
        self.Instruction = instr

    def to_string(self):
        ret = ''
        ret += str(self.I1)
        ret += str(self.I2)
        return ret


class IntegerQueue:
    def __init__(self):
        self.queue = defaultdict(list)
        # self.queue['ALU1']
        self.current_size = 0
        self.MAX_SIZE = 16

    def add2queue(self, tp, busy_bit_table, register_map, instruction):
        print '#### Integer Queue ####'
        if tp is 'ALU1' or tp is 'ALU2':
            self.current_size += 1

            # Checking if there's enough space in the queue for a new instruction
            if self.current_size == self.MAX_SIZE:
                self.current_size -= 1
                # I guess an exception is fine for now...
                raise Exception('Integer Queue can only hold'
                                ' up to 16 instructions')
            else:

                print 'rt:', instruction.rt, register_map.isMapped(instruction.rt)
                print 'rs:', instruction.rs, register_map.isMapped(instruction.rs)

                # Adding the current instruction to the Integer Queue
                rec = IntegerQueueRecord(register_map.isMapped(instruction.rt),
                                         register_map.isMapped(instruction.rs),
                                         busy_bit_table, instruction)
                self.queue[tp].append(rec)
        else:
            raise Exception('Integer Queue can only hold'
                            ' instructions that intend to '
                            'go to either ALU1 or ALU2')

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


