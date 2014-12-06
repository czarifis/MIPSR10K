'''
Created on Dec 5, 2014

@author: Costas Zarifis
'''


class FPADD1:
    def __init__(self):
        pass

    def calc(self, df, active_list):
        list_tuple = active_list.fp_queue_pop('FPADD')
        if list_tuple is None:
            print 'Cannot de-queue from FPADD list'
        else:
            print 'dequeueing from FPADD'


    def edge(self, df, dfMap, active_list):
        pass