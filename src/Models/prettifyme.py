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
    def printme(self,df,output):
        with open(output, 'w') as f:
            f.write(self.HEADER)
            f.write(df.to_html(classes='df'))
            f.write(self.FOOTER)
