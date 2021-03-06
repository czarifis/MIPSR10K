'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''


'''
This class provides all the functionality for Issuing instructions
'''


class Issue:
    def __init__(self):
        self.currInstrs = {}
        self.currIssuedInstrs = []
        self.issue_times = 0
        self.clc = 0
        self.mispredicted = False
        self.mispredicted_data = None

    def calc(self, df, pipeline_register, active_list, args, MISPREDICT):

        if pipeline_register == 0:
            self.issue_times = args.issue
            self.currIssuedInstrs = []

            about2go2execution_units = self.access_queue2get_one_instr_for_each_exe_unit(active_list)
            for k in about2go2execution_units:
                self.currIssuedInstrs.append(about2go2execution_units[k].Instruction)

            instrz = active_list.go_over_queues()
            self.currIssuedInstrs = self.currIssuedInstrs + instrz
            if MISPREDICT is not None:
                self.mispredicted = True
                self.mispredicted_data = MISPREDICT
                return None

            return about2go2execution_units


        # if instructions is not None:
        #     # print instructions
        #     # Inst = ins.Instruction()
        #
        #
        #     self.currInstrs = dict(self.currInstrs.items()+instructions.items())
        #
        #     d4 = dict(self.currInstrs)
        #     d4.update(instructions)
        #     self.currInstrs = d4
        #
        #     self.iterOverInstructions(activeList, args)
        #
        #     return 0
        # return -1


    # This function iterates over n instructions at each cycle
    def iterOverInstructions(self, activeList, args, MISPREDICT):
        it = 0
        about_to_be_deleted = []
        for instr in sorted(self.currInstrs):
            actualInstr = self.currInstrs[instr]

            try:
                # activeList.process_issue(actualInstr)
                activeList.process_add2queue(actualInstr)
                self.currIssuedInstrs[instr] = actualInstr
                about_to_be_deleted.append(instr)

                it += 1
                if it == args.issue:
                    break
            except Exception, e:
                print 'ecxeption at issue clock:', self.clc, e

        for ii in about_to_be_deleted:
            del self.currInstrs[ii]

    # This function tries to access the corresponding queues so that it returns
    # one instruction for each execution unit
    def access_queue2get_one_instr_for_each_exe_unit(self, active_list):
        d = {}
        list_tuple = active_list.fp_queue_pop('FPMUL')
        if list_tuple is None:
            # print 'Cannot de-queue from FPMUL list'
            # Let's try to de-queue from the FPADD list
            list_tuple = active_list.fp_queue_pop('FPADD')
            if list_tuple is None:
                # print 'Cannot de-queue from FPADD list'
                pass
            else:
                # print 'dequeueing from FPMUL'
                d['FP1'] = list_tuple
                # return list_tuple

        else:
            # print 'dequeueing from FPMUL'
            d['FP1'] = list_tuple
            # return list_tuple

        list_tuple = active_list.fp_queue_pop('FPADD')
        if list_tuple is None:
            # print 'Cannot de-queue from FPADD list'
            # Let's try to de-queue from the FPADD list
            list_tuple = active_list.fp_queue_pop('FPMUL')
            if list_tuple is None:
                # print 'Cannot de-queue from FPMUL list'
                pass
            else:
                # print 'dequeueing from FPADD'
                d['FP2'] = list_tuple
                # return list_tuple

        else:
            # print 'dequeueing from FPADD'
            d['FP2'] = list_tuple
            # return list_tuple

        ######

        list_tuple = active_list.int_queue_pop('ALU1')
        if list_tuple is None:
            # print 'Cannot de-queue from ALU2 list'
            # Let's try to de-queue from the FPADD list
            list_tuple = active_list.int_queue_pop('ALU2')
            if list_tuple is None:
                # print 'Cannot de-queue from ALU2 list'
                pass
            else:
                # print 'dequeueing from ALU2'
                d['ALU1'] = list_tuple
                # return list_tuple

        else:
            # print 'dequeueing from ALU1'
            d['ALU1'] = list_tuple
            # return list_tuple

        list_tuple = active_list.int_queue_pop('ALU2')
        if list_tuple is None:
            # print 'Cannot de-queue from ALU2 list'
            # Let's try to de-queue from the FPADD list
            list_tuple = active_list.fp_queue_pop('ALU1')
            if list_tuple is None:
                # print 'Cannot de-queue from ALU1 list'
                pass
            else:
                # print 'dequeueing from ALU1'
                d['ALU2'] = list_tuple
                # return list_tuple

        else:
            # print 'dequeueing from ALU2'
            d['ALU2'] = list_tuple
            # return list_tuple

        list_tuple = active_list.address_queue_pop()
        if list_tuple is None:
            # print 'Cannot de-queue from address point queue'
            # Let's try to de-queue from the FPADD list
            pass
        else:
            # print 'dequeueing from address point queue'
            d['A'] = list_tuple
            # return list_tuple

        return d

    def edge(self, df, dfMap, activeList):
        self.clc += 1


        if self.currIssuedInstrs:
            for k in self.currIssuedInstrs:
                if self.mispredicted is True and self.mispredicted_data['line'] < k.line_number:
                    df.xs(k.line_number)[str(self.clc)] = 'X'


                else:
                    df.xs(k.line_number)[str(self.clc)] = 'II'
        if self.mispredicted is True:
            # We need to remove all instructions with line number later
            # than the branch's from the queue
            activeList.issue_mispredict(self.mispredicted_data)
            self.mispredicted_data = None
            self.mispredicted = False
            pass


                # print 'registered an ID stage on location:', k, self.clc

            # empty the "queue"
            # self.currInstrs = None

            # dfMap.xs(0)[self.clc] = activeList.map.prettyTable()