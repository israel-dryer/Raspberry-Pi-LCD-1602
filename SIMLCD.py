###########################################
## Simulated LCD Screen for Testing
## File     : SIMLCD.py
## Author   : Israel Dryer
## Written  : 2019-09-11
###########################################
from os import system

class SimulatedLCD:
    
    HLINE = '|'+'~'*16+'|'
    VLINE1 = '|{}|'
    VLINE2 = '|{}|'

    def __init__(self):
        pass

    def print_msg(self, msg1='', msg2=''):
        system('cls')
        msg1 = msg1[:16]
        msg2 = msg2[:16]
        pad1 = (16-len(msg1))//2
        line1 = (' '*pad1 + msg1 + ' '*pad1).ljust(16)    
        pad2 = (16-len(msg2))//2
        line2 = (' '*pad2 + msg2 + ' '*pad2).ljust(16)    

        print(self.HLINE)
        print(self.VLINE1.format(line1))
        print(self.VLINE2.format(line2))
        print(self.HLINE)

