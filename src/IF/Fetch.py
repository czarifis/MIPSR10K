'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''


'''
This class provides all the functionality for fetching instructions
'''
class Fetch:

    def __init__(self):
        self.i = 0
        self.currInstrs = {}
        self.clc = 0
        self.mispredicted = False
        self.mispredicted_data = None

    # Fetching 4 lines per click
    def fetch_n_linesPerClck(self, df, args):
        self.currInstrs = {}
        for line in args.filename:
            currLineStr = line.strip() 
            # print( currLineStr )
            # self.currInstrs.append(currLineStr)
            self.i += 1
            # print 'current line:', self.i
            self.currInstrs[self.i] = (self.i, currLineStr)
            # print 'line',line
            if self.i % args.issue == 0:
                return self.currInstrs
        # These are the last lines which have not been returned so far
        return self.currInstrs
        # print df.head()

    def calc(self, df, args, active_list, MISPREDICT):
        # print 'Fetch calc'
        # ret = None
        # if self.mispredicted is True:
        #     pass
        # else:
        ret = {}
        if self.mispredicted is False:
            ret = self.fetch_n_linesPerClck(df, args)
        else:
            # print 'need to re-fetch instructions'
            record = active_list.branch_stack.pop()
            ret = active_list.return_instructions_after_branch(record.mispredicted_branch)
            self.mispredicted = False
            self.currInstrs = ret

            # print record
            pass

        if MISPREDICT is not None:
                self.mispredicted = True
                self.mispredicted_data = MISPREDICT
                return None

        # print 'IF calc:',ret
        return ret

    def edge(self, df, dfMap):
        self.clc += 1
        a = ['' for n in range(self.clc)]
        if self.clc>1:
            df[str(self.clc)] = ' '
            dfMap[self.clc] = ' '
        elif self.clc==1:
            dfMap.loc[1] = ['Register Map Table:'] + a
            dfMap.loc[2] = ['Active List:'] + a
            dfMap.loc[3] = ['Busy Bit Tables:'] + a
            dfMap.loc[4] = ['Notes:'] + a
            dfMap.loc[5] = ['Integer Queue:'] + a
            dfMap.loc[6] = ['FP Queue:'] + a
            dfMap.loc[7] = ['Address Queue:'] + a
        
        for k in sorted(self.currInstrs.keys()):
            df.loc[k] = [self.currInstrs[k], '', ''] + a
            if self.mispredicted is True and self.mispredicted_data['line'] < k:
                df.xs(k)[str(self.clc)] = 'X'
            else:
                df.xs(k)[str(self.clc)] = 'IF'
            # print 'registered an IF stage on location:', k, self.clc

        # dfMap.loc[1] = a 
        # dfMap.xs(1)[self.clc] = 'a'
       
        # print 'Fetch edge'


    def readInsts(self):
        pass
