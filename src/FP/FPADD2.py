'''
Created on Dec 5, 2014

@author: Costas Zarifis
'''


class FPADD2:
    def __init__(self):
        self.clc = 0
        self.curr_instr = None


    def calc(self, df, FPADD1FPADD2, active_list):
        self.curr_instr = FPADD1FPADD2
        if FPADD1FPADD2 is not None:
            active_list.fp_queue.make_available('FPADD', FPADD1FPADD2.prd)
            active_list.integer_queue.make_available('ALU2', FPADD1FPADD2.prd)
            pass
        return self.curr_instr

    def edge(self, df, dfMap, active_list):
        self.clc += 1
        if self.curr_instr is not None:
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'FPADD2'


            # empty the "queue"
            # self.currInstrs = None