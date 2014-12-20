'''
Created on Nov 30, 2014

@author: Costas Zarifis
'''
class Instruction:

    def __init__(self, line, instr):
        self.op = None  # This is the opcode of the instruction. It's one of the {L,S,I,B,A,M}
        self.rs = None  # source register 1
        self.rt = None  # source register 2
        self.rd = None  # destination register
        self.prd = None  # physical destination register assigned during first stage of execution
        self.prt = None  # physical source register 2 assigned during first stage of execution
        self.prs = None  # physical source register 1 assigned during first stage of execution
        self.clean_soon = [] # list with instructions about to get freed on commit
        self.extra = None  # extra/immediate
        self.initial_instr = instr
        self.ROB = []
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
        self.comment = '' # comment next to command after char : '#'
        self.decoding = '' # the decoded instruction is going to be added as a comment
        self.MappedDecoding = '' # The decoded instruction with the mapped physical registers
        self.line_number = line

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
    def add2Comment(self,comment):
        # print 'soon to be comment:', str(self.comment)+str(comment)
        self.comment = str(self.comment)+str(comment)

    def add2MappedDecoding(self, mappedDec):
        # print 'soon to be mapped:',mappedDec
        self.MappedDecoding = str(mappedDec)[1:-1].replace("'","").replace(",","")


    def add2Decoding(self,dec):
        self.decoding = ''.join(dec[1:-1]).replace("'","").replace(",","")

    def printInstr(self):
        if self.op == 'L':
            ret = self.rt,'<-',self.extra,'(',self.rs,')'
            # print self.rt,'<-',self.extra,'(',self.rs,')'
        elif self.op == 'S':
            ret = self.rt,'->',self.extra,'(',self.rs,')'
        elif self.op == 'I':
            ret = self.rd,'<-',self.rs,'INTOP',self.rt
        elif self.op == 'A':
            ret = self.rd,'<-',self.rs,'FPADD',self.rt
        elif self.op == 'M':
            ret = self.rd,'<-',self.rs,'FPMUL',self.rt
        elif self.op == 'B':
            ret = 'BEQ,',self.rs,',',self.rt,',xx,',self.prediction
        ret = str(ret)#''.join(ret)
        self.add2Decoding(ret)
        # print ret
        return ret

    def clear_instruction(self):
        pass

    def toStr(self):
        ret = self.decoding
        return ret

    def toMappedStr(self,map):
        # print 'map',map
        return self.MappedDecoding