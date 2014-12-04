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
       
            

    def edge(self,df,dfMap):
        self.clc+=1
        a = ['' for n in range(self.clc)]
        if self.clc>1:
            df[self.clc] = ' '
            dfMap[self.clc] = ' '
        elif self.clc==1:
            dfMap.loc[1] = ['Register Map Table'] + a 


        
       
        for k in self.currInstrs.keys():
            
            
            df.loc[k] = [self.currInstrs[k]] + a 

            df.xs(k)[self.clc] = 'IF'

        # dfMap.loc[1] = a 
        # dfMap.xs(1)[self.clc] = 'a'
       
        # print 'Fetch edge'


    def readInsts(self):
        pass
