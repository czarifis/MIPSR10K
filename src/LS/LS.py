'''
Created on Dec 16, 2014

@author: Costas Zarifis
'''


'''
This class provides all the functionality for executing Load Store instructions
'''


class LS:
    def __init__(self):
        self.currInstrs = {}
        self.currIssuedInstrs = []
        self.issue_times = 0
        self.clc = 0

    def calc(self, df, pipeline_register, active_list, args):

        # if pipeline_register == 0:
        self.issue_times = args.issue
        self.currIssuedInstrs = []
        ls_about2execute = self.dequeue_ls2execute(active_list)
        if ls_about2execute is not None:
            self.currIssuedInstrs.append(ls_about2execute.Instruction)
            active_list.integer_queue.make_available('ALU2', ls_about2execute.Instruction.prt)
            active_list.integer_queue.make_available('ALU1', ls_about2execute.Instruction.prt)
            active_list.fp_queue.make_available('FPADD', ls_about2execute.Instruction.prt)
            active_list.fp_queue.make_available('FPMUL', ls_about2execute.Instruction.prt)
            active_list.address_queue.make_available(ls_about2execute.Instruction.prt)



            # That's for LS unit only:
            # active_list.address_queue.make_address_available(ls_about2execute.Instruction.extra)



            active_list.set_rob_record2done(ls_about2execute.Instruction.line_number)

            # instrz = active_list.go_over_queues()
            # self.currIssuedInstrs = self.currIssuedInstrs + instrz
            # return ls_about2execute



    # This function tries to access the corresponding queues so that it returns
    # one instruction for each execution unit
    def dequeue_ls2execute(self, active_list):

        list_tuple = active_list.address_queue_pop2execute()
        if list_tuple is None:
            # print 'Cannot de-queue from (LS) address point queue'
            pass
            # Let's try to de-queue from the FPADD list
        else:
            # print 'dequeueing from address point queue'
            return list_tuple
            # return list_tuple

        return None

    def edge(self, df, dfMap, activeList):
        self.clc += 1
        if self.currIssuedInstrs:
            for k in self.currIssuedInstrs:
                df.xs(k.line_number)[str(self.clc)] = 'LS'
            self.currIssuedInstrs = []


