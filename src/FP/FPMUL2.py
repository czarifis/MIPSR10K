'''
Created on Dec 7, 2014

@author: Costas Zarifis
'''


class FPMUL2:
    def __init__(self):
        self.clc = 0
        self.curr_instr = None


    def calc(self, df, FPMUL1FPMUL2, active_list, MISPREDICT):
        self.curr_instr = FPMUL1FPMUL2
        if FPMUL1FPMUL2 is not None:
            if MISPREDICT is not None:
                self.mispredicted = True
                return None
            active_list.fp_queue.make_available('FPADD', FPMUL1FPMUL2.prd)
            active_list.fp_queue.make_available('FPMUL', FPMUL1FPMUL2.prd)
            active_list.integer_queue.make_available('ALU2', FPMUL1FPMUL2.prd)
            active_list.integer_queue.make_available('ALU1', FPMUL1FPMUL2.prd)
            active_list.address_queue.make_available(FPMUL1FPMUL2.prd)
            pass
        return self.curr_instr

    def edge(self, df, dfMap, active_list):
        self.clc += 1
        if self.curr_instr is not None:
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'FP2(II)'


            # empty the "queue"
            # self.currInstrs = None