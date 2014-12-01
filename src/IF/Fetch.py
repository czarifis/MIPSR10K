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

    # Fetching 4 lines per click
    def fetch4linesPerClck(self,df,args):
        self.currInstrs = {}
        for line in args.filename:
            currLineStr = line.strip() 
            print( currLineStr )
            # self.currInstrs.append(currLineStr)
            self.i+=1
            self.currInstrs[self.i] = currLineStr
            
            if self.i%4==0:
                return self.currInstrs
        # print df.head()

    def calc(self,df,args):
        # print 'Fetch calc'
        ret = self.fetch4linesPerClck(df,args)
        return ret
       
            

    def edge(self,df):
        self.clc+=1
        if self.clc>1:
            df[self.clc] = ' '

        for k in self.currInstrs.keys():
            a = ['' for n in range(self.clc)]
            
            df.loc[k] = [self.currInstrs[k]] + a 

            df.xs(k)[self.clc] = 'IF'
       
        # print 'Fetch edge'


    def readInsts(self):
        pass
