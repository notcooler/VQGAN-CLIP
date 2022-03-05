from colorama import Fore, Back, Style
import os

class Choice:
    def __init__(self, name_):
        self.name = name_

    def getName(self):
        return self.name

def printAllChoice(choices:list=None):
    if choices != None:
        msgToSend = ""
        count = 1
        for choice in choices:
            msgToSend += f"{Fore.CYAN}[{Fore.RED}{str(count)}{Fore.CYAN}] {Fore.WHITE}{choice.getName()}\n"
            count+=1
        
        print(msgToSend[:-1])