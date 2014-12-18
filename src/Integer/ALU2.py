'''
Created on Dec 13, 2014

@author: Costas Zarifis
'''


class ALU2:
    def __init__(self):
        self.clc = 0
        self.curr_instr = None
        self.prev_dest = None
        self.miss = False

    def calc(self, df, active_list, reg, mispredict):


        # if after_issue == 0:
        self.curr_instr = None
        # record = self.access_queue(active_list)
        if 'ALU2' in reg.keys():
            record = reg['ALU2']
        else:
            record = None
        if record is not None:
            ins = record.Instruction
            # ins.prd = active_list.map.isMapped(ins.rd)
            # ins.prs = active_list.map.isMapped(ins.rs)
            # ins.prt = active_list.map.isMapped(ins.rt)
            ins.rs = record.I1
            ins.rs = record.I2

            self.curr_instr = ins

            active_list.integer_queue.make_available('ALU2', ins.prd)
            active_list.integer_queue.make_available('ALU1', ins.prd)
            active_list.fp_queue.make_available('FPADD', ins.prd)
            active_list.fp_queue.make_available('FPMUL', ins.prd)
            active_list.address_queue.make_available(ins.prd)


            self.prev_dest = ins.prd
            active_list.set_rob_record2done(ins.line_number)
            # pass
        else:
            if self.prev_dest is not None:
                active_list.integer_queue.make_available('ALU1', self.prev_dest)
        return self.curr_instr


    def edge(self, df, dfMap, active_list):
        self.clc += 1


        if self.curr_instr is not None:
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'ALU2'

        if self.miss is True:
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'X'

            # empty the "queue"
            # self.currInstrs = None