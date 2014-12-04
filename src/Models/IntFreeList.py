class FreeList:

    def __init__(self):
        self.list = []
        for i in range(64):
            self.list.append('I'+str(i))

    '''
        This function assigns(returns and removes from the list) a physical register.
        If the list is empty it returns None 
    '''
    def assign(self):
        try:
            assigned = self.list[0]
            self.list.remove(assigned)
            return assigned
        except:
            return None

    '''
        This function returns 4 registers in parallel or 
        None if there are not 4 of them free
    '''
    def assign4InParallel(self):
        ret = []
        for i in range(4):
            assigned = self.assign()
            if assigned == None:
                # Hmm the instruction requires 4 registers
                # but there are not 4 registers available
                return None
            ret.append(assigned)
        return ret



    '''
        This function frees (adds to the list) the registers that are contained inside the list l
    '''
    def free(self,l):
        assert isinstance(l,list)
        for e in l:
            self.list.append(e)

    '''
        This is similar to the previous one but for a single register
    '''
    def freeReg(self,r):
        self.list.append(r)

if __name__ == '__main__':
    l = FreeList()
    print l.list
    r = l.assign()
    print 'assigned:',r
    print l.list
    r2 = l.assign()
    print 'assigned:',r2
    l.free([r])
    print l.list
    l.assign4InParallel()