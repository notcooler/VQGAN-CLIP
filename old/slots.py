from plugins.util import *
from plugins.Args import Args
from plugins.choice import Choice, printAllChoice
import sys
sys.path.append("./")
from main import runMain

def slot():
    print(f"{Fore.YELLOW}Loading...")
    wait(0.5)
    setConsoleSize(23, 71)
    wait(1)
    while True:
        clear()
        print(slotsLogo)
        slots = [
            Choice("Slot 1."),
            Choice("Slot 2."),
            Choice("Slot 3."),
            Choice("Slot 4."),
            Choice("Slot 5."),
            Choice("Back."),
        ]
        print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
        printAllChoice(slots)
        print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
        choiceStr = input(f'{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: {Fore.RED}')
        if choiceStr.isnumeric():
            choiceInt = int(choiceStr)
            if choiceInt < len(slots)+1:
                if choiceInt != 6:
                    'a'
                else:
                    setConsoleSize()
                    clear()
                    runMain()
                    break 