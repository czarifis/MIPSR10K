'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''


'''
This class provides all the functionality for Issuing instructions
'''


class Issue:
    def __init__(self):
        self.currInstrs = None
        self.currIssuedInstrs = {}
        self.clc = 0

    def calc(self, df, instructions, activeList):
        if instructions is not None:
            # print instructions
            # Inst = ins.Instruction()

            self.currInstrs = instructions
            self.iterOverInstructions(activeList)

    # This function iterates over 4 instructions at each cycle
    def iterOverInstructions(self, activeList):
        for instr in self.currInstrs:
            actualInstr = self.currInstrs[instr]

            self.currIssuedInstrs[instr] = actualInstr
            activeList.process_issue(actualInstr)


    def edge(self, df, dfMap, activeList):
        self.clc += 1
        # print 'Issue edge'
        dfMap.xs(1)[self.clc] = activeList.map.toString()
        dfMap.xs(2)[self.clc] = activeList.ROBToString()
        dfMap.xs(3)[self.clc] = activeList.busy_bit_tables.to_string()
        dfMap.xs(4)[self.clc] = activeList.map.Note
        dfMap.xs(5)[self.clc] = activeList.integer_queue.to_string()
        dfMap.xs(6)[self.clc] = activeList.fp_queue.to_string()

        if self.currInstrs is not None:
            for k in self.currInstrs.keys():



                df.xs(k)[str(self.clc)] = 'II'
                # print 'registered an ID stage on location:', k, self.clc

            # empty the "queue"
            self.currInstrs = None

            # dfMap.xs(0)[self.clc] = activeList.map.prettyTable()