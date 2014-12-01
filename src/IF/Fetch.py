'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''


'''
This class provides all the functionality for fetching instructions
'''
class Fetch:
    def calc(self,args):
        print 'Fetch calc'
        i = 0
        for line in args.filename:
            print( line.strip() )
            i+=1
            if i%4==0:
                break
            

    def edge(self):
        print 'Fetch edge'


    def readInsts(self):
        pass
