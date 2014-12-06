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
import II.Issue as II
import FP.FPADD1 as FPADD1
import argparse
import pandas as pd 
import numpy as np
import Models.prettifyme as pr
import Models.ActiveList as ActiveList


class Main:
    def __init__(self):
        self.clc = 0
        self.IFIDReg = None
        self.IDIIReg = None
        self.ActiveList = ActiveList.ActiveList()

    def calc(self, df, args, IfStage, IdStage, IiStage, FPADD1Stage):
        # print 'global calc'
        
        instructions = IfStage.calc(df,args)
        # if self.clc > 1:
        # print self.IFIDReg

        # Passing the IF/ID register (which holds the instructions)
        # and the Active List (ROB)
        instructions2 = IdStage.calc(df, self.IFIDReg, self.ActiveList)
        self.IFIDReg = instructions
        # Passing the ID/II register (which holds the instructions)
        # and the Active List (ROB)
        IiStage.calc(df, self.IDIIReg, self.ActiveList)
        # print '##### Instructions:',instructions,'#####'
        self.IDIIReg = instructions2

        FPADD1Stage.calc(df, self.ActiveList)

    def edge(self, df, dfMap, IfStage, IdStage, IiStage, FPADD1Stage):
        # print 'call the edge function of each stage'
        IfStage.edge(df, dfMap)
        # if self.clc > 1:
        IdStage.edge(df, dfMap, self.ActiveList)
        IiStage.edge(df, dfMap, self.ActiveList)
        FPADD1Stage.edge(df, dfMap, self.ActiveList)



# main function 
if __name__ == '__main__':

    # Declaring Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', dest="filename", type=argparse.FileType('r'), help='input file path', required=False)
    parser.add_argument('-out', dest="output", type=str, help='output file path', required=False)
    args = parser.parse_args()

    # Checking if input argument is given
    if args.filename is None:
        # if not add the default input file
        args.filename = open('benchmarks/default.txt', 'r')
        
    # Checking if output argument is given
    if args.output is None:
        args.output = 'output'
    
    df = pd.DataFrame(columns=('Instruction', 'Logical', 'Physical', '1'))
    dfMap = pd.DataFrame(columns=('Clock Counter', '1'))

    # Initializing stages
    m = Main()
    IfStage = IF.Fetch()
    IdStage = ID.Decode()
    IiStage = II.Issue()
    FPADD1Stage = FPADD1.FPADD1()
    # while True:
    
    # compute number of clocks (might need to do sth better than this)
    clocks = sum(1 for line in args.filename)+10
    print 'clocks',clocks

    # reset file pointer
    args.filename.seek(0)

    for i in range(clocks):
        m.clc = i+1
        m.calc(df, args, IfStage, IdStage, IiStage, FPADD1Stage)
        m.edge(df, dfMap, IfStage, IdStage, IiStage, FPADD1Stage)
    
    # class providing printing functionality
    pm = pr.prettifyme()
    
    pm.printme(df, dfMap, args.output)
    # pm.printme(dfMap, 'map'+args.output+'.json')