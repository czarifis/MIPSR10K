'''
Created on Dec 17, 2014

@author: Costas Zarifis
'''

from collections import defaultdict

# Class that describes a record inside the integer queue


class StackRecord:
    def __init__(self, rob, branch):
        self.ROB = rob
        self.mispredicted_branch = branch


    # to_string method used to "pretty print" the output into a matrix
    def to_string(self):
        ret = ''
        ret += '{('+self.ROB+')}'
        return ret

# Class describing the Integer Queue


class BranchStack:
    def __init__(self):

        self.stack = []
        self.current_size = 0
        self.MAX_SIZE = 4

    # Adding record to stack queue
    def add2stack(self, err):
        rob = err['ROB']
        instr = err['branch']
        branch_line = err['line']
        print '#### Branch Stack ####'
        # if tp is 'L' or tp is 'S':
        self.current_size += 1
        # Checking if there's enough space in the stack for a new record
        if self.current_size > self.MAX_SIZE:
            self.current_size -= 1
            # I guess an exception is fine for now...
            raise Exception('Branch stack can only hold'
                            ' up to 4 records')
        else:
            rec = StackRecord(rob, instr)
            self.stack.append(rec)


    # This function is used by the LS execution unit to pop instructions in order
    def pop(self):
        if not self.stack:
            # No elements exist in the corresponding stack
            return None
        else:
            e = self.stack[0]
            self.stack.remove(e)
            self.current_size -= 1
            return e

    def to_string(self):
        if self.current_size == 0:
            return 'empty!'
        ret = ''
        ret += '[ '
        for e in self.stack:
            ret += e.to_string()+' '
        ret += ']'

        return ret


