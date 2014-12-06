'''
Created on Dec 5, 2014

@author: Costas Zarifis
'''


class FPADD3:
    def __init__(self):
        self.clc = 0
        self.curr_instr = None

    def calc(self, df, pipeline_register, active_list):
        self.curr_instr = pipeline_register

        if pipeline_register is not None:
            active_list.fp_queue.make_available('FPADD', pipeline_register.prd)
            pass
        return self.curr_instr

    def edge(self, df, dfMap, active_list):
        self.clc += 1
        if self.curr_instr is not None:
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'FPADD3'


            # empty the "queue"
            # self.currInstrs = None