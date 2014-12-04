'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''
class Instruction:

    def __init__(self,instr):
        self.op = None # This is the opcode of the instruction. It's one of the {L,S,I,B,A,M}
        self.rs = None # source register 1
        self.rt = None # source register 2
        self.rd = None # destination register
        self.extra = None # extra/immediate
        '''
            TODO: 
            If the extra field is 0, it means after execution the branch were correctly 
            predicted and the trace file is run correctly. If the extra field is 1, when the 
            branch finished execution, it finds out that it was mis-predicted, so it will flush 
            instructions after the branch. Now it goes back to same branch instruction, but the 
            extra field is changed to 0 (simulator must do this), so it re-runs the branch and 
            instructions afterwards. It is just a model that the instructions on the wrong path 
            of the branch are exactly the same as the correct path.
        '''
        self.prediction = None 
        self.comment = None # comment next to command after char : '#'

        # Create a hash for easier access and less confusion :)
        self.getVal = {
            'destination'   : self.rd,
            'source1'       : self.rs,
            'source2'       : self.rt,
            'operation'     : self.op,
            'op'            : self.op,
            'opcode'        : self.op,
            'IMM'           : self.extra,
            'imm'           : self.extra,
            'immed'         : self.extra,
            'immediate'     : self.extra,
            'prediction'    : self.prediction,
            'extra'         : self.prediction,
            'comment'       : self.comment
        }

        # {L,S,I,B,A,M} = {load,store,integer,branch,fpadd,fpmul}
        self.getOpName = {
            'L' : 'Load',
            'S' : 'Store',
            'I' : 'Integer',
            'B' : 'Branch',
            'A' : 'Fpadd',
            'M' : 'Fpmul'
        }

        firstSplit = instr.split('#')
        try:
            self.comment = firstSplit[1]
        except:
            # No comment was given
            self.comment = None


        # print 'comment is:',self.comment
        instruction = firstSplit[0]
        instructionElems = instr.split(' ')
        op = instructionElems[0]
        # print 'opcode is:', op
        self.op = op
        if op == 'L':
            # This is a load instruction
            self.rt = 'r'+str(int(instructionElems[2],16))
            self.rs = 'r'+str(int(instructionElems[1],16))
            self.extra = instructionElems[4]
        elif op == 'S':
            # This is a store instruction
            self.rt = 'r'+str(int(instructionElems[2],16))
            self.rs = 'r'+str(int(instructionElems[1],16))
            self.extra = instructionElems[4]
        elif op == 'I':
            self.rs = 'r'+str(int(instructionElems[1],16))
            self.rt = 'r'+str(int(instructionElems[2],16))
            self.rd = 'r'+str(int(instructionElems[3],16))
        elif op == 'A':
            self.rs = 'r'+str(int(instructionElems[1],16))
            self.rt = 'r'+str(int(instructionElems[2],16))
            self.rd = 'r'+str(int(instructionElems[3],16))
        elif op == 'M':
            self.rs = 'r'+str(int(instructionElems[1],16))
            self.rt = 'r'+str(int(instructionElems[2],16))
            self.rd = 'r'+str(int(instructionElems[3],16))
        elif op == 'B':
            self.rs = 'r'+str(int(instructionElems[1],16))
            self.rt = 'r'+str(int(instructionElems[2],16))
            self.prediction = instructionElems[4]

        # pass

    def printInstr(self):
        if self.op == 'L':
            print self.rt,'<-',self.extra,'(',self.rs,')'
        elif self.op == 'S':
            print self.rt,'->',self.extra,'(',self.rs,')'
        elif self.op == 'I':
            print self.rd,'<-',self.rs,'INTOP',self.rt
        elif self.op == 'A':
            print self.rd,'<-',self.rs,'FPADD',self.rt
        elif self.op == 'M':
            print self.rd,'<-',self.rs,'FPMUL',self.rt
        elif self.op == 'B':
            print 'BEQ,',self.rs,',',self.rt,',xx,',self.prediction



