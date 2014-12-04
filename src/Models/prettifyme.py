'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''

class prettifyme:
    def __init__(self):
        self.HEADER =   '''
                            <html>
                                <head>
                                    <style>
                                        
                                    </style>
                                </head>
                                <body>
                                    
                        '''

        self.FOOTER =   '''
                                    
                                </body>
                            </html>
                        '''
    '''
        This function outputs the structures maintained by this program to CSV files
    '''
    def printme(self,df,dfmap,output):
        # with open(output, 'w') as f:
        #     f.write(self.HEADER)
        #     f.write(df.to_html(classes='df',escape=False,col_space=10))
        #     f.write(self.FOOTER)
        df.to_csv(output+'.csv')
        dfmap.to_csv('map'+output+'.csv')
        # self.csv2HTMLTable(output+'.csv')
        # from pandas import ExcelWriter
        # writer = ExcelWriter('output.xlsx')
        # df.to_excel(writer,'Sheet1')
        # writer.save()
        self.finalize(output)

    '''
        This function generates html tables from the partial CSV files
    '''
    def finalize(self,output):
        import sys
        import os
        import csv
        import string
        table_string = ""
        with open( output+'.csv', 'rb') as csvfile:
            reader = csv.reader( csvfile )
            table_string += '<table border=\"1\">'
            for row in reader:
                table_string += "<tr>" + \
                                  "<td>" + \
                                      string.join( row, "</td><td>" ) + \
                                  "</td>" + \
                                "</tr>"
            table_string += '</table><table border=\"1\">'
        with open( 'map'+output+'.csv', 'rb') as csvfile:
            
            reader = csv.reader( csvfile )
            
            for row in reader:
                table_string += "<tr>" + \
                                  "<td>" + \
                                      string.join( row, "</td><td>" ) + \
                                  "</td>" + \
                                "</tr>"

            table_string += '</table>'
            
            # sys.stdout.write( table_string )
        with open(output+'.html', 'w') as f:
            f.write(self.HEADER)
            f.write(table_string)
            f.write(self.FOOTER)
