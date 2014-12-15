'''
Created on Dec 7, 2014

@author: Costas Zarifis
'''


class FPMUL1:
    def __init__(self):
        self.clc = 0
        self.curr_instr = None

    def calc(self, df, active_list, reg):
        # if after_issue == 0:
        self.curr_instr = None
        # record = self.access_queue(active_list)



        if 'FP2' in reg.keys():
            record = reg['FP2']
        else:
            record = None


        if record is not None:
            ins = record.Instruction
            # ins.prd = active_list.map.isMapped(ins.rd)
            # ins.prs = active_list.map.isMapped(ins.rs)
            # ins.prt = active_list.map.isMapped(ins.rt)
            ins.rs = record.I1
            ins.rs = record.I2
            active_list.fp_queue.make_available('FPADD', ins.prd)
            active_list.fp_queue.make_available('FPMUL', ins.prd)
            active_list.integer_queue.make_available('ALU2', ins.prd)
            active_list.integer_queue.make_available('ALU1', ins.prd)

            self.curr_instr = ins
            # pass
        return self.curr_instr



    def access_queue(self, active_list):
        list_tuple = active_list.fp_queue_pop('FPMUL')
        if list_tuple is None:
            print 'Cannot de-queue from FPMUL list'
        else:
            print 'dequeueing from FPMUL'
            return list_tuple


        return None


    def edge(self, df, dfMap, active_list):
        self.clc += 1
        if self.curr_instr is not None:
            # pass
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'FP2(I)'


            # empty the "queue"
            # self.currInstrs = None