'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''


'''
This class provides all the functionality for decoding instructions
'''
class Decode:

    def __init__(self):
        self.i = 0
        self.currInstrs = {}
        self.clc = 1

    

    def calc(self,df,instructions):
        # print 'Decode calc'
        if instructions is not None:
            print instructions
            self.currInstrs = instructions
        pass
        
       
            

    def edge(self,df):
        self.clc+=1
        print 'Decode edge'

        for k in self.currInstrs.keys():
            
            print k,self.clc
            df.xs(k)[self.clc] = 'ID'

        # empty the "queue"
        self.currInstrs = {}
       
        


    def readInsts(self):
        pass
