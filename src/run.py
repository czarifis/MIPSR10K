'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''
import IF.Fetch as IF
import argparse
 



def calc():
    print 'call appropriate stage'
    IfStage = IF.Fetch()
    IfStage.calc()

def edge():
    print 'call the edge function of each stage'
    IfStage = IF.Fetch()
    IfStage.edge()

if __name__ == '__main__':
    # main function 
   

    parser = argparse.ArgumentParser()
    parser.add_argument('filename',  type=argparse.FileType('r'), help='input file path')
    args = parser.parse_args()

    for line in args.filename:
        print( line.strip() )

    # while True:
    # for i in range(15):
    #     calc()
    #     edge()
    