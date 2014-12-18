'''
Created on Dec 7, 2014

@author: Costas Zarifis
'''


class FPMUL3:
    def __init__(self):
        self.clc = 0
        self.curr_instr = None

    def calc(self, df, pipeline_register, active_list):
        self.curr_instr = pipeline_register

        if pipeline_register is not None:

            active_list.fp_queue.make_available('FPADD', pipeline_register.prd)
            active_list.fp_queue.make_available('FPMUL', pipeline_register.prd)
            active_list.integer_queue.make_available('ALU2', pipeline_register.prd)
            active_list.integer_queue.make_available('ALU1', pipeline_register.prd)
            active_list.address_queue.make_available(pipeline_register.prd)

            active_list.set_rob_record2done(pipeline_register.line_number)

        return self.curr_instr


    def edge(self, df, dfMap, active_list):
        self.clc += 1
        if self.curr_instr is not None:
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'FP2(III)'


            # empty the "queue"
            # self.currInstrs = None