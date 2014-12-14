'''
Created on Dec 2, 2014

@author: Costas Zarifis
'''


class FreeList:

    def __init__(self):
        self.list = []  # List with free physical registers

        # Created separate busyBitTables structure instead
        # self.busy = {}  # This dict keeps whether a physical register is busy or not

        # Physical Registers range from 1 to 64
        for i in range(1, 65):
            self.list.append('I'+str(i))

            # Created separate busyBitTables structure instead
            # self.busy['I'+str(i)] = False

    '''
        This function assigns(returns and removes from the list) a physical register.
        If the list is empty it returns None 
    '''
    def assign(self, source = None):
        if source == None:
            print 'Assigning a new physical register'
            try:
                assigned = self.list[0]
                self.list.remove(assigned)

                # Created separate busyBitTables structure instead
                # self.busy[assigned] = True
                return assigned
            except:
                # We're out of physical registers
                return None
        else:
            print 'assignment error'
        

    '''
        This function returns 4 registers in parallel or 
        None if there are not 4 of them free
    '''
    def assign4InParallel(self):
        ret = []
        for i in range(4):
            assigned = self.assign()
            if assigned is None:
                # Hmm the instruction requires 4 registers
                # but there are not 4 registers available
                return None
            ret.append(assigned)
        return ret



    '''
        This function frees (adds to the list) the registers that are contained inside the list l
    '''
    def free(self, l):
        assert isinstance(l, list)
        for e in l:
            self.freeReg(e)

    '''
        This is similar to the previous one but for a single register
    '''
    def freeReg(self, r):
        self.list.append(r)

        # Created separate busyBitTables structure instead
        # self.busy[r] = False

if __name__ == '__main__':
    l = FreeList()
    print l.list
    r = l.assign()
    print 'assigned:', r
    print l.list
    r2 = l.assign()
    print 'assigned:', r2
    l.free([r])
    print l.list
    l.assign4InParallel()