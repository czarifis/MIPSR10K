'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''
import IF.Fetch as IF
import argparse
import pandas as pd 
import numpy as np
import Models.prettifyme as pr


def calc(df,args):
    print 'global calc'
    IfStage = IF.Fetch()
    IfStage.calc(df,args)


def edge():
    print 'call the edge function of each stage'
    IfStage = IF.Fetch()
    IfStage.edge()



if __name__ == '__main__':
    # main function 
   
    # Declaring Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-in' ,dest="filename" ,type=argparse.FileType('r'), help='input file path', required=False)
    parser.add_argument('-out' ,dest="output" ,type=str, help='output file path', required=False)
    args = parser.parse_args()

    # Checking if input argument is given
    if args.filename == None:
        # if not add the default input file
        args.filename = open('benchmarks/default.txt', 'r')
        

    print args.filename
    df = pd.DataFrame(np.random.randn(2, 2)) 
    
    
    # while True:
    for i in range(2):
        calc(df,args)
        edge()
    
    # class providing printing functionalities
    pm = pr.prettifyme()
    
    # Checking if output argument is given
    if args.output != None:
        pm.printme(df, args.output)
    else:
        pm.printme(df,'output.html')
    