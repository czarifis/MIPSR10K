'''
Created on Dec 16, 2014

@author: Costas Zarifis
'''

class A:
    def __init__(self):
        self.clc = 0
        self.curr_instr = None
        # self.prev_input = []

    def calc(self, df, active_list, reg):
        # if after_issue == 0:
        self.curr_instr = None
        # record = self.access_queue(active_list)
        if 'A' in reg.keys():
            record = reg['A']
        else:
            record = None

        if record is not None:
            ins = record.Instruction
            # ins.prd = active_list.map.isMapped(ins.rd)
            # ins.prs = active_list.map.isMapped(ins.rs)
            # ins.prt = active_list.map.isMapped(ins.rt)
            ins.rs = record.I1
            ins.rs = record.I2
            active_list.address_queue_address_of_line_is_ready(ins)


            self.curr_instr = ins
            return 0


            # pass
        return -1

    def edge(self, df, dfMap, active_list):
        self.clc += 1
        if self.curr_instr is not None:
            # pass
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'A'


            # empty the "queue"
            # self.currInstrs = None
