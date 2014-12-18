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
import FP.FPADD2 as FPADD2
import FP.FPADD3 as FPADD3
import FP.FPMUL1 as FPMUL1
import FP.FPMUL2 as FPMUL2
import FP.FPMUL3 as FPMUL3
import LS.A as A
import LS.LS as LS
import WB.WriteBack as WB
import Integer.ALU1 as ALU1
import Integer.ALU2 as ALU2
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
        self.FPADD1FPADD2 = None
        self.FPADD2FPADD3 = None
        self.FPMUL1FPMUL2 = None
        self.FPMUL2FPMUL3 = None
        self.AFTERISSUE = {}
        self.ALSReg = -1
        self.ActiveList = ActiveList.ActiveList()

    def calc(self, df, args, IfStage, IdStage,
             IiStage, FPADD1Stage, FPADD2Stage,
             FPADD3Stage, WBStage, ALU1Stage,
             FPMUL1Stage, FPMUL2Stage, FPMUL3Stage,
             ALU2Stage, AStage, LSStage):
        # print 'global calc'
        
        instructions = IfStage.calc(df, args)
        # if self.clc > 1:
        # print self.IFIDReg




        # Passing the ID/II register (which holds the instructions)
        # and the Active List (ROB)
        # Also passing the args as it keeps information about the number
        # of instructions that can be issued per cycle


        WBStage.calc(df, self.ActiveList)

        FPADD1Instr = None

        # if self.AFTERISSUE == 0:
        issue_res = IiStage.calc(df, self.IDIIReg, self.ActiveList, args)

        # Let's put FPADD1 first... It's a timing thing...
        FPADD1Instr = FPADD1Stage.calc(df, self.ActiveList, self.AFTERISSUE)
        FPMUL1Instr = FPMUL1Stage.calc(df, self.ActiveList, self.AFTERISSUE)

        ALU1Stage.calc(df, self.ActiveList, self.AFTERISSUE)
        ALU2Stage.calc(df, self.ActiveList, self.AFTERISSUE)


        # df, self.IDIIReg, self.ActiveList, args
        # df, self.ActiveList, self.AFTERISSUE
        LSStage.calc(df, self.ALSReg, self.ActiveList, args)

        Astage_output = AStage.calc(df, self.ActiveList, self.AFTERISSUE)


        # issue_res = None
        # print '##### Instructions:',instructions,'#####'
        # Passing the IF/ID register (which holds the instructions)
        # and the Active List (ROB)
        instructions2 = IdStage.calc(df, self.IFIDReg, self.ActiveList)
        self.IFIDReg = instructions
        self.ALSReg = Astage_output



        self.IDIIReg = instructions2

        # if not self.AFTERISSUE:
        #     if not issue_res :
        #         self.AFTERISSUE = {}
        #     else:
        #         self.AFTERISSUE = issue_res
        #         self.AFTERISSUE['wasEmpty'] = True
        # else:
        #     if not issue_res:
        #         self.AFTERISSUE = {}
        #         self.AFTERISSUE['wasEmpty'] = False
        #     else:
        #         self.AFTERISSUE = issue_res
        #         self.AFTERISSUE['wasEmpty'] = False
        if issue_res is None:
            self.AFTERISSUE = {}
        else:
            self.AFTERISSUE = issue_res






        FPADD2Instr = FPADD2Stage.calc(df, self.FPADD1FPADD2, self.ActiveList)
        self.FPADD1FPADD2 = FPADD1Instr

        FPMUL2Instr = FPMUL2Stage.calc(df, self.FPMUL1FPMUL2, self.ActiveList)
        self.FPMUL1FPMUL2 = FPMUL1Instr

        FPADD3Stage.calc(df, self.FPADD2FPADD3, self.ActiveList)
        self.FPADD2FPADD3 = FPADD2Instr

        FPMUL3Stage.calc(df, self.FPMUL2FPMUL3, self.ActiveList)
        self.FPMUL2FPMUL3 = FPMUL2Instr









    def edge(self, df, dfMap, IfStage, IdStage,
             IiStage, FPADD1Stage, FPADD2Stage,
             FPADD3Stage, WBStage, ALU1Stage,
             FPMUL1Stage, FPMUL2Stage, FPMUL3Stage,
             ALU2Stage, AStage, LSStage):
        # print 'call the edge function of each stage'
        IfStage.edge(df, dfMap)
        # if self.clc > 1:
        IdStage.edge(df, dfMap, self.ActiveList)
        IiStage.edge(df, dfMap, self.ActiveList)
        FPADD1Stage.edge(df, dfMap, self.ActiveList)
        FPADD2Stage.edge(df, dfMap, self.ActiveList)
        FPADD3Stage.edge(df, dfMap, self.ActiveList)
        FPMUL1Stage.edge(df, dfMap, self.ActiveList)
        FPMUL2Stage.edge(df, dfMap, self.ActiveList)
        FPMUL3Stage.edge(df, dfMap, self.ActiveList)
        ALU1Stage.edge(df, dfMap, self.ActiveList)
        ALU2Stage.edge(df, dfMap, self.ActiveList)
        AStage.edge(df, dfMap, self.ActiveList)
        LSStage.edge(df, dfMap, self.ActiveList)
        WBStage.edge(df, dfMap, self.ActiveList)



# main function 
if __name__ == '__main__':

    # Declaring Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', dest="filename", type=argparse.FileType('r'), help='input file path', required=False)
    parser.add_argument('-out', dest="output", type=str, help='output file path', required=False)
    parser.add_argument('-issue', dest="issue", type=int, help='total number of instructions that can get '
                                                               'issued (default is 1)', required=False)
    args = parser.parse_args()

    # Checking if input argument is given
    if args.filename is None:
        # if not add the default input file
        args.filename = open('benchmarks/default.txt', 'r')
        
    # Checking if output argument is given
    if args.output is None:
        args.output = 'output'

    # Checking if issue argument is given
    if args.issue is None:
        args.issue = 4
    
    df = pd.DataFrame(columns=('Instruction', 'Logical', 'Physical', '1'))
    dfMap = pd.DataFrame(columns=('Clock Counter', '1'))

    # Initializing stages
    m = Main()
    IfStage = IF.Fetch()
    IdStage = ID.Decode()
    IiStage = II.Issue()
    FPADD1Stage = FPADD1.FPADD1()
    FPADD2Stage = FPADD2.FPADD2()
    FPADD3Stage = FPADD3.FPADD3()
    FPMUL1Stage = FPMUL1.FPMUL1()
    FPMUL2Stage = FPMUL2.FPMUL2()
    FPMUL3Stage = FPMUL3.FPMUL3()

    ALU1Stage = ALU1.ALU1()
    LSStage = LS.LS()
    AStage = A.A()
    ALU2Stage = ALU2.ALU2()
    WBStage = WB.WriteBack()
    # while True:
    
    # compute number of clocks (might need to do sth better than this)
    # clocks = sum(1 for line in args.filename)+100
    clocks = 50
    print 'clocks', clocks

    # reset file pointer
    args.filename.seek(0)

    for i in range(clocks):
        m.clc = i+1
        m.calc(df, args, IfStage, IdStage, IiStage,
               FPADD1Stage, FPADD2Stage, FPADD3Stage,
               WBStage, ALU1Stage, FPMUL1Stage,
               FPMUL2Stage, FPMUL3Stage, ALU2Stage,
               AStage, LSStage)
        m.edge(df, dfMap, IfStage, IdStage, IiStage,
               FPADD1Stage, FPADD2Stage, FPADD3Stage,
               WBStage, ALU1Stage, FPMUL1Stage,
               FPMUL2Stage, FPMUL3Stage, ALU2Stage,
               AStage, LSStage)
    
    # class providing printing functionality
    pm = pr.prettifyme()
    
    pm.printme(df, dfMap, args.output)
    # pm.printme(dfMap, 'map'+args.output+'.json')