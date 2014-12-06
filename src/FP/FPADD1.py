'''
Created on Dec 5, 2014

@author: Costas Zarifis
'''


class FPADD1:
    def __init__(self):
        self.clc = 0
        self.curr_instr = None


    def calc(self, df, active_list):
        self.curr_instr = None
        record = self.access_queue(active_list)
        if record is not None:
            ins = record.Instruction
            # ins.prd = active_list.map.isMapped(ins.rd)
            # ins.prs = active_list.map.isMapped(ins.rs)
            # ins.prt = active_list.map.isMapped(ins.rt)
            ins.rs = record.I1
            ins.rs = record.I2

            self.curr_instr = ins
            # pass
        return self.curr_instr



    def access_queue(self, active_list):
        list_tuple = active_list.fp_queue_pop('FPADD')
        if list_tuple is None:
            print 'Cannot de-queue from FPADD list'
        else:
            print 'dequeueing from FPADD'
            return list_tuple
        return None


    def edge(self, df, dfMap, active_list):
        self.clc += 1
        if self.curr_instr is not None:
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'FPADD1'


            # empty the "queue"
            # self.currInstrs = None