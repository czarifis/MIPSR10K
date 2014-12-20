'''
Created on Dec 5, 2014

@author: Costas Zarifis
'''


class ALU1:
    def __init__(self):
        self.clc = 0
        self.curr_instr = None
        self.prev_dest = None
        self.miss = False
        self.mispredicted = False
        self.mispredicted_data = None

    def calc(self, df, active_list, reg, MISPREDICT):
        # if after_issue == 0:
        self.curr_instr = None
        # record = self.access_queue(active_list)
        if 'ALU1' in reg.keys():
            record = reg['ALU1']
        else:
            record = None
        if record is not None:
            ins = record.Instruction
            # ins.prd = active_list.map.isMapped(ins.rd)
            # ins.prs = active_list.map.isMapped(ins.rs)
            # ins.prt = active_list.map.isMapped(ins.rt)
            # ins.rs = record.I1
            # ins.rs = record.I2





            self.curr_instr = ins
            if MISPREDICT is not None:
                self.mispredicted = True
                self.mispredicted_data = MISPREDICT
                return None
            if self.miss:
                return

            if ins.prediction == '1':
                err = {}
                err['line'] = ins.line_number
                err['branch'] = ins
                err['ROB'] = ins.ROB
                # active_list.ROB = ins.ROB
                active_list.add2Branch_stack(err)
                # active_list.set_rob_record2done(ins.line_number)
                return err

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
                active_list.integer_queue.make_available('ALU2', self.prev_dest)
        # return self.curr_instr

    def access_queue(self, active_list):
        list_tuple = active_list.int_queue_pop('ALU2')
        if list_tuple is None:
            print 'Cannot de-queue from ALU2 list'
        else:
            print 'dequeueing from ALU2'
            return list_tuple

        return None

    def edge(self, df, dfMap, active_list):
        self.clc += 1
        if self.curr_instr is not None:
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'ALU1'
        if self.mispredicted is True:
            self.mispredicted = False
            df.xs(self.curr_instr.line_number)[str(self.clc)] = 'X'


            # empty the "queue"
            # self.currInstrs = None