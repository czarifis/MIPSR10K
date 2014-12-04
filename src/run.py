'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''

'''
Note: According to this: https://groups.google.com/forum/#!searchin/cse-240a-fa14/re-order$20buffer/cse-240a-fa14/GY-_iQot_NI/E1zRTGOojvQJ
ROB == Active list

'''


# Imports
import IF.Fetch as IF
import ID.Decode as ID
import argparse
import pandas as pd 
import numpy as np
import Models.prettifyme as pr
class Main:
    def __init__(self):
        self.clc = 0
        self.IFIDReg = None

    def calc(self,df,args,IfStage,IdStage):
        # print 'global calc'
        
        instructions = IfStage.calc(df,args)
        # if self.clc > 1:
        # print self.IFIDReg
        IdStage.calc(df,self.IFIDReg)

        self.IFIDReg = instructions


    def edge(self,df,IfStage,IdStage):
        # print 'call the edge function of each stage'
        IfStage.edge(df)
        # if self.clc > 1:
        IdStage.edge(df)



# main function 
if __name__ == '__main__':
    
   
    # Declaring Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-in' ,dest="filename" ,type=argparse.FileType('r'), help='input file path', required=False)
    parser.add_argument('-out' ,dest="output" ,type=str, help='output file path', required=False)
    args = parser.parse_args()

    # Checking if input argument is given
    if args.filename == None:
        # if not add the default input file
        args.filename = open('benchmarks/default.txt', 'r')
        
    # Checking if output argument is given
    if args.output == None:
        args.output = 'output.html'
    
    df = pd.DataFrame(columns=('Instruction','1')) 
    

    # Initializing stages
    m = Main()
    IfStage = IF.Fetch()
    IdStage = ID.Decode()
    # while True:
    
    # compute number of clocks (might need to do sth better than this)
    clocks = sum(1 for line in args.filename)
    print 'clocks',clocks

    # reset file pointer
    args.filename.seek(0)

    for i in range(clocks):
        m.clc = i+1
        m.calc(df,args,IfStage,IdStage)
        m.edge(df,IfStage,IdStage)
    
    # class providing printing functionalities
    pm = pr.prettifyme()
    
    pm.printme(df, args.output)