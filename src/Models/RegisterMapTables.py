class RegisterMapTables:
    def __init__(self):
        self.LogToPhy = {}
        self

        for i in range(32):
            self.LogToPhy['r'+str(i)] = 'I'+str(i)

    def setLog2Phy(self,log,phy):
        self.LogToPhy[log]=phy


    def prettyTable(self, cssClass=''):
        dictionary = self.LogToPhy
        ''' pretty prints a dictionary into an HTML table(s) '''
        if isinstance(dictionary, str):
            return '<td>' + dictionary + '</td>'
        s = ['<table ']
        if cssClass != '':
            s.append('class="%s"' % (cssClass))
        s.append('>\n')
        for key, value in dictionary.iteritems():
            s.append('<tr>\n  <td valign="top"><strong>%s</strong></td>\n' % str(key))
            if isinstance(value, dict):
                if key == 'picture' or key == 'icon':
                    s.append('  <td valign="top"><img src="%s"></td>\n' % Page.prettyTable(value, cssClass))
                else:
                    s.append('  <td valign="top">%s</td>\n' % Page.prettyTable(value, cssClass))
            elif isinstance(value, list):
                s.append("<td><table>")
                for i in value:
                    s.append('<tr><td valign="top">%s</td></tr>\n' % Page.prettyTable(i, cssClass))
                s.append('</table>')
            else:
                if key == 'picture' or key == 'icon':
                    s.append('  <td valign="top"><img src="%s"></td>\n' % value)
                else:
                    s.append('  <td valign="top">%s</td>\n' % value)
            s.append('</tr>\n')
        s.append('</table>')
        return '\n'.join(s)

    def toString(self):
        s = ''
        for k in self.LogToPhy.keys():
            s = s+' '+str(k)+':'+str(self.LogToPhy[k])+''
        return s
