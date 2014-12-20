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
                                <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <a class="navbar-brand" target="_blank" href="http://zarifis.info">Costas Zarifis </a>
        </div>
        <div>
          <ul class="nav navbar-nav">
            <li><a href="#timeline">Timeline</a></li>
            <li><a href="#1">Register Mapping</a></li>
            <li><a href="#2">Active List</a></li>
            <li><a href="#3">Busy Bit</a></li>
            <li><a href="#4">Integer Queue</a></li>
            <li><a href="#5">FP Queue</a></li>
            <li><a href="#5">Address Queue</a></li>
            <li><a href="#code">Trace File</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
          <p class="nav navbar-text">CSE 240A - Graduate Computer Architecture</p>

        </ul>
        </div>
      </div>
    </nav>
                                    
                        '''

        self.FOOTER =   '''
                                    
                                </body>
                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap-theme.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
<style type="text/css">
    .bs-example{
    	margin: 20px;
    }
    body { padding-top: 70px; }
</style>
                            </html>
                        '''
    '''
        This function outputs the structures maintained by this program to CSV files
    '''
    def printme(self,df,dfmap,args):
        output = args.output
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
        self.finalize(args)

    '''
        This function generates html tables from the partial CSV files
    '''
    def finalize(self, args):
        output = args.output
        input = args.filename
        import sys
        import os
        import csv
        import string
        table_string = ""
        with open( output+'.csv', 'rb') as csvfile:
            reader = csv.reader( csvfile )

            table_string += '<table id="timeline" class="table table-hover table-bordered ">'
            for row in reader:
                table_string += "<tr>" + \
                                  "<td>" + \
                                      string.join( row, "</td><td>" ) + \
                                  "</td>" + \
                                "</tr>"
            table_string += '</table><table class="table table-hover table-bordered">'
        with open( 'map'+output+'.csv', 'rb') as csvfile:
            
            reader = csv.reader( csvfile )

            i = 0
            for row in reader:

                table_string += "<tr id=\""+str(i) + \
                                  "\"><td>" + \
                                      string.join( row, "</td><td>" ) + \
                                  "</td>" + \
                                "</tr>"
                i += 1

            table_string += '</table>'

        table_string += '<H3 id="code">Trace File: </H3><br/><div>' \
                        '<table id="timeline" class="table table-hover ' \
                        'table-bordered "><tr><td>'

        args.filename.seek(0)
        counter = 0
        for line in args.filename:
            counter += 1
            currLineStr = line.strip()
            table_string += str(counter) + ' '
            table_string += currLineStr
            table_string += '<br/>'
        table_string +='</td></tr></table></div>'
            
            # sys.stdout.write( table_string )
        with open(output+'.html', 'w') as f:
            f.write(self.HEADER)
            f.write(table_string)
            f.write(self.FOOTER)
