'''
Created on Dec 6, 2014

@author: Costas Zarifis
'''


class WriteBack:
    def __init__(self):
        self.clc = 0
        self.curr_instrs = None


    def calc(self, df, active_list):
        self.curr_instrs = None
        record = self.access_rob(active_list)
        if record is not None:
            self.curr_instrs = record
            # pass


            pass
        return self.curr_instrs

    def access_rob(self, active_list):
        if self.clc == 10:
            print 'boom'
            pass
        list_inst = active_list.pop_from_active_list()
        if not list_inst:
            print 'Cannot write back'
        else:
            print 'removing from active list'
            return list_inst
        return None

    def free_from_busy_bit(self, active_list):
        for e in self.curr_instrs:
            active_list.busy_bit_tables.setAsNonBusy(e.prd)

    def add2free_list(self, active_list):
        for e in self.curr_instrs:
            active_list.freeList.freeReg(e.prd)

    def make_address_available(self, active_list):
        for e in self.curr_instrs:
            if e.op == 'S':
                active_list.address_queue.make_address_available(e.extra)






    def edge(self, df, dfMap, active_list):
        self.clc += 1
        if self.curr_instrs is not None:

            for i in self.curr_instrs:

                df.xs(i.line_number)[str(self.clc)] = 'C'

            self.make_address_available(active_list)


