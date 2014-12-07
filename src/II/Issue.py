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
        self.currIssuedInstrs = {}
        self.issue_times = 0
        self.clc = 0

    def calc(self, df, instructions, activeList, args):
        self.issue_times = args.issue
        self.currIssuedInstrs = {}
        if instructions is not None:
            # print instructions
            # Inst = ins.Instruction()


            self.currInstrs = dict(self.currInstrs.items()+instructions.items())

            d4 = dict(self.currInstrs)
            d4.update(instructions)
            self.currInstrs = d4

            self.iterOverInstructions(activeList, args)




    # This function iterates over 4 instructions at each cycle
    def iterOverInstructions(self, activeList, args):
        it = 0
        about_to_be_deleted = []
        for instr in sorted(self.currInstrs):
            actualInstr = self.currInstrs[instr]


            try:
                activeList.process_issue(actualInstr)
                self.currIssuedInstrs[instr] = actualInstr
                about_to_be_deleted.append(instr)

                it += 1
                if it == args.issue:
                    break
            except Exception, e:
                print 'BOOM clock:', self.clc, e

        for ii in about_to_be_deleted:
            del self.currInstrs[ii]



    def edge(self, df, dfMap, activeList):
        self.clc += 1
        # print 'Issue edge'
        # dfMap.xs(1)[self.clc] = activeList.map.toString()
        # dfMap.xs(2)[self.clc] = activeList.ROBToString()
        # dfMap.xs(3)[self.clc] = activeList.busy_bit_tables.to_string()
        # dfMap.xs(4)[self.clc] = activeList.map.Note
        # dfMap.xs(5)[self.clc] = activeList.integer_queue.to_string()
        # dfMap.xs(6)[self.clc] = activeList.fp_queue.to_string()
        if self.currIssuedInstrs:
            for k in sorted(self.currIssuedInstrs.keys()):
                df.xs(k)[str(self.clc)] = 'II'


                # print 'registered an ID stage on location:', k, self.clc

            # empty the "queue"
            # self.currInstrs = None

            # dfMap.xs(0)[self.clc] = activeList.map.prettyTable()