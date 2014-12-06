'''
Created on Dec 5, 2014

@author: Costas Zarifis
'''


class busyBitTables:

    # Constructor
    def __init__(self):
        self.table = {}

        # True for verbose results, False for concise results
        self.VERBOSE = False

        for i in range(1, 65):
            self.table['I'+str(i)] = False

    # set a physical register's busy bit table to True
    def setAsBusy(self, key):
        self.table[key] = True

    # set a physical register's busy bit table to False
    def setAsNonBusy(self, key):
        self.table[key] = False

    # This function checks if the physical register is busy or not
    def isBusy(self, key):
        return self.table[key]

    # This function returns a string representation of the busy bit tables
    # edit the self.VERBOSE field to make the string representation more or
    # less verbose.
    def to_string(self):
        ret = ''
        # Check if VERBOSE mode is enabled
        if self.VERBOSE:
            for i in range(1, 65):
                ret += 'I'+str(i)+':'+str(self.table['I'+str(i)])+' '

        else:
            for i in range(1, 65):
                # Only print the current records if it's busy
                if self.table['I'+str(i)]:
                    ret += 'I'+str(i)+':'+str(self.table['I'+str(i)])+' '
        return ret