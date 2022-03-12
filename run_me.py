from plugins.util import printPerChar, clear
clear()
printPerChar("Starting Application...\nVersion: 1.0beta")
import os
import sys
import webbrowser
import subprocess as sub
import json
try:
    import pretty_errors
except ImportError:
    pass
import shutil
import requests
import glob
from tqdm.auto import tqdm
from time import sleep
from colorama import Fore, Back, Style
from plugins.choice import Choice, printAllChoice
from plugins.Args import Args

from plugins.util import startBanner, clear, getPlatform, setConsoleSize, wait, logo, setupLogo, models, slotsLogo
#import generator

def downloadModel():
    while True:
        clear()
        print(setupLogo)
        print(f"{Fore.YELLOW}Choose a AI image to download!(Imagenet_16382 is probably the best)\nBut they all produce other results!")
        print(f'{Fore.BLUE}─'*os.get_terminal_size().columns)
        printAllChoice(models)
        print(f'{Fore.BLUE}─'*os.get_terminal_size().columns)
        choiceStr = input(f'{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: {Fore.RED}')
        if choiceStr.isnumeric():
            choiceInt = int(choiceStr)
            if choiceInt < len(models)+1 and choiceInt != 0:
                clear()
                print(setupLogo)
                model = models[choiceInt-1]
                print(f'{Fore.BLUE}─'*os.get_terminal_size().columns)
                print(f"{Fore.YELLOW}Downloading {model.getName()}.yaml{Fore.BLUE}")
                with requests.get(model.getLinks()[0], stream=True) as r:
                    total_length = int(r.headers.get("Content-Length"))
                    with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                        with open(f"./models/{model.getName()}.yaml", 'wb') as output:
                            shutil.copyfileobj(raw, output)
                
                print(f"{Fore.YELLOW}Downloading {model.getName()}.ckpt{Fore.BLUE}")
                with requests.get(model.getLinks()[1], stream=True) as r:
                    total_length = int(r.headers.get("Content-Length"))
                    with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                        with open(f"./models/{model.getName()}.ckpt", 'wb') as output:
                            shutil.copyfileobj(raw, output)
                print(f'{Fore.BLUE}─'*os.get_terminal_size().columns)
                print(f"{Fore.LIGHTGREEN_EX}Successfully downloaded {model.getName()}!")
                break
                

def downloadLibs():
    clear()
    print(f"{Fore.RED}Make sure you have homebrew installed!\nIf not do ctrl+c to exit!\nOr find a way to install \"{Fore.YELLOW}exempi{Fore.RED}\", not my prob\n\n{Fore.BLUE}(you can hit enter if you want to install the other libaries!){Fore.YELLOW}Hit enter to continue")
    input('')
    wait(2)
    clear()
    print(setupLogo)
    red = Fore.RED
    yellow = Fore.YELLOW
    white = Fore.WHITE

    try:
        print(f"{white}Starting process...")

        print(f"{yellow}Downloading CLIP...{Style.RESET_ALL}")
        sub.call("git clone https://github.com/openai/CLIP".split(' '))
        
        print(f"{yellow}Downloading VQGAN..{Style.RESET_ALL}.")
        sub.call("git clone https://github.com/CompVis/taming-transformers".split(' '))

        # print(f"{yellow}Creating venv..{Style.RESET_ALL}.")
        # try:
        #     cmd = "python3 -m venv env"
        #     cmd2 = ["source ./env/bin/activate"]
        #     if getPlatform() == "win": cmd = "py -m venv env"
        #     if getPlatform() == "win": cmd2 = [".\env\Scripts\\activate.bat"]
        #     sub.call(cmd.split(' '))
        #     sub.call(cmd2)
        # except OSError as e:
        #     print(e)
        #     print(f"{red}Couldn't create a venv, please create it manually!\n{white}Command: {cmd}")
        #     os._exit(0)

        # sub.call("".split(' '))
        print(f"{yellow}Downloading all pip libraries!{Style.RESET_ALL}")
        sub.call("pip install -r ./requirements.txt".split(' '))
        a = "python3"
        if getPlatform() == "win": a="py"
        sub.call(f"{a} -m pip install --upgrade pillow".split(' '))

        print(f"{yellow}Downloading exempi...{Style.RESET_ALL}")
        sub.call("brew install exempi".split(' '))

        print(f"{Fore.LIGHTGREEN_EX}Successfully completed process!")
        sub.call("python3 libinstalled.py".split(' '))
        os._exit(0)
    except TypeError:
        pass
        os._exit(0)
    except Exception as e:
        print(red+e)
        print(f"{red}An error occured...")
        os._exit(0)

def runsetup():
    print(f"{Fore.YELLOW}Loading...")
    wait(0.5)
    setConsoleSize(23, 72)
    wait(1)
    while True:
        clear()
        print(setupLogo)
        print(f"TIP: Type \'back\' to go back to the main menu!")
        choice = input(f"{Fore.WHITE}Do you want to install the libraries or download a model? {Fore.WHITE}({Fore.GREEN}libs{Fore.WHITE}/{Fore.RED}model{Fore.WHITE})\n{Fore.WHITE}> {Fore.BLUE}")
        if choice.lower() == "model":
            downloadModel()
            break
        elif choice.lower() == "libs":
            downloadLibs()
            break
        elif choice.lower() == "back":
            setConsoleSize()
            print("a")
            clear()
            runMain()
            break

def selectModel():
    avalaibleModels = []
    files = glob.glob("./models/*.yaml")
    for file_ in files:
        avalaibleModels.append(Choice(os.path.basename(file_)[:-5]))
    if avalaibleModels == []:
        print(f"{Fore.RED}There is no download module in ./models, please download one by going to the setup menu!\nOr reading readme.md!")
        sleep(4)
        setConsoleSize()
        clear()
        runMain()
    else:
        while True:
            clear()
            print(slotsLogo)
            print(f"{Fore.WHITE}Whihc ai model do you want to use?")
            print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
            printAllChoice(avalaibleModels)
            print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
            choiceStr = input(f'{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: {Fore.RED}')
            if choiceStr.isnumeric():
                choiceInt = int(choiceStr)
                if choiceInt < len(avalaibleModels)+1 and choiceInt != 0:
                    return avalaibleModels[choiceInt-1].getName()

def editSlot(slotCount):
    clear()
    print(slotsLogo)
    print(f"{Fore.YELLOW}Read readme.md if you want your art generator to correctly work")
    print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
    args = Args(
        selectModel(),
        input(f"{Fore.WHITE}What should the ai generate (e.g. \'a house in the forest\')?{Fore.MAGENTA}"),
        input(f"{Fore.WHITE}Image width(higher = better and slower): {Fore.MAGENTA}"),
        input(f"{Fore.WHITE}Image height(higher = better and slower): {Fore.MAGENTA}"),
        50,
        input(f"{Fore.WHITE}What seed you want it to be(-1 for random): {Fore.MAGENTA}"),
        input(f"{Fore.WHITE}What should be the max iterations(-1 for until you press ctrl+c)? {Fore.MAGENTA}"),
        f"./scripts/slots/slot{slotCount}.json"
    )
    while True:
        clear()
        print(args.getAll())
        b = input(f"{Fore.YELLOW}Do you confirm this? {Fore.WHITE}({Fore.GREEN}y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE})\n{Fore.WHITE}> {Fore.BLUE}")
        if b.lower() == "y":
            return args
        elif b.lower() == "n":
            runSlot()
            break

def saveSlotToJson(args, slotJson, slotCount):
    clear()
    print(slotsLogo)
    print(f"{Fore.YELLOW}Saving data to slot {slotCount}...{Style.RESET_ALL}")
    try:
        slotJson.clear()

        defaultWidth = 512
        defaultHeight = 512
        defaultInterval_image = 50
        defaultSeed = -1
        defaultMax_iterations = -1

        width = 0
        height = 0
        interval_image = 0
        seed = 0
        max_iterations = 0

        if args.width.isnumeric(): width = args.width
        if args.height.isnumeric(): height = args.height
        if args.interval_image.isnumeric(): interval_image = args.interval_image
        if args.seed.isnumeric(): seed = args.seed
        if args.max_iterations.isnumeric(): max_iterations = args.max_iterations

        if width == 0: width = defaultWidth
        if height == 0: height = defaultHeight
        if interval_image == 0: interval_image = defaultInterval_image
        if seed == 0: seed = defaultSeed
        if max_iterations == 0: max_iterations = defaultMax_iterations

        toAppend = {
            "model": args.model,
            "prompts": args.prompts,
            "width": width,
            "height": height,
            "interval_image": interval_image,
            "seed": seed,
            "max_iterations": max_iterations
        }
        slotJson.append(toAppend)

        slotFileWrite = open(f"./scripts/slots/slot{str(slotCount)}.json", 'w')
        json.dump(slotJson, slotFileWrite)
        slotFileWrite.close()
        print(f"{Fore.LIGHTGREEN_EX}Successfully saved slot {slotCount}!")

    except Exception as e:
        print(e)
        print(f"{Fore.RED}An error occured...")
        os._exit(0)

def selectSlot(slotCount):
    clear()
    print(slotsLogo)
    print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
    print(f"Checking if slot{slotCount} is empty...")
    slotFileRead = open(f"./scripts/slots/slot{str(slotCount)}.json", 'r')
    slotJson = json.loads(slotFileRead.read())
    if slotJson != []:
        while True:
            clear()
            print(slotsLogo)
            a=input(f"{Fore.RED}Slot {slotCount} isn't empty do you want to overwrite it? {Fore.WHITE}({Fore.GREEN}y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE})\n{Fore.WHITE}> {Fore.BLUE}")
            if a.lower() == "y":
                args = editSlot(slotCount)
                saveSlotToJson(args, slotJson, slotCount)
                slotFileRead.close()
                sleep(2.7)
                setConsoleSize()
                clear()
                runMain()
                break
            elif a.lower() == "n":
                setConsoleSize()
                clear()
                runSlot()
                break
    else:
        args = editSlot(slotCount)
        saveSlotToJson(args, slotJson, slotCount)
        slotFileRead.close()
        sleep(2.7)
        setConsoleSize()
        clear()
        runMain()

    

def runSlot():
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
            if choiceInt < len(slots)+1 and choiceInt != 0:
                if choiceInt == 6:
                    setConsoleSize()
                    clear()
                    runMain()
                    break
                else:
                    selectSlot(choiceInt)
                    break

def getPath():
    return os.path.abspath("./")

plt = getPlatform()
allChoices = [
    Choice("Get the original code."),
    Choice("Setup the workspace."),
    Choice("Edit slots."),
    Choice("Run the art generator!"),
    Choice("Discord."),
    Choice("Exists the application.")
]
try:

    setConsoleSize()
    wait(1)
    clear()

    print(startBanner)
    wait(5)
    clear()

    def runMain():
        print(logo)
        print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
        printAllChoice(allChoices)
        print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
        choice = input(f'{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: {Fore.RED}')

        if choice == "1":
            webbrowser.open("https://colab.research.google.com/drive/1lx9AGsrh7MlyJhK9UrNTK8pYpARnx457", 1)
            clear()
            runMain()
        elif choice == "2":
            clear()
            print(f"{Fore.GREEN}Redirecting you to setup.py...")
            wait(1)
            runsetup()
        elif choice == "3":
            clear()
            print(f"{Fore.GREEN}Redirecting you to setup.py...")
            wait(1)
            print(f"{Fore.YELLOW}Loading...")
            wait(0.5)
            setConsoleSize(23, 71)
            wait(1)
            runSlot()
        elif choice == "4":
            clear()
            print(logo)
            print(f"{Fore.YELLOW}Getting all slots...")
            slotsChoices = []
            files = glob.glob("./scripts/slots/*.json")
            count = 1
            for file_ in files:
                with open(file_, 'r') as _file:
                    data = json.load(_file)
                    if data != []:
                        slotsChoices.append(Choice(f"Slot {count}."))
                        count+=1
            if slotsChoices == []:
                clear()
                print(f"{Fore.RED}There is no slots to read right now!\nMake a new slot from the main menu and choose option 3!")
                sleep(6)
                clear()
                runMain()
            else:
                while True:
                    clear()
                    print(logo)
                    print(f"TIP: Type \'back\' to go back to the main menu!")
                    print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
                    printAllChoice(slotsChoices)
                    print(f'{Fore.MAGENTA}─'*os.get_terminal_size().columns)
                    choiceStr = input(f'{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Choice: {Fore.RED}')
                    if choiceStr == "back":
                        clear()
                        runMain()
                        break
                    elif choiceStr.isnumeric():
                        choiceInt = int(choiceStr)
                        if choiceInt < len(slotsChoices)+1 and choiceInt != 0:
                            slotFileRead = open(f"./scripts/slots/slot{str(choiceInt)}.json", 'r')
                            slotJson = json.loads(slotFileRead.read())
                            args = Args(
                                slotJson[0]["model"],
                                slotJson[0]["prompts"],
                                slotJson[0]["width"],
                                slotJson[0]["height"],
                                slotJson[0]["interval_image"],
                                slotJson[0]["seed"],
                                slotJson[0]["max_iterations"],
                                f"./scripts/slots/slot{choiceInt}.json",
                            )
                            while True:
                                clear()
                                print(args.getAll())
                                b = input(f"{Fore.YELLOW}Do you confirm this? {Fore.WHITE}({Fore.GREEN}y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE})\n{Fore.WHITE}> {Fore.BLUE}")
                                if b.lower() == "y":
                                    clear()
                                    print(logo)
                                    print(args.getAll())
                                    print(f"{Fore.MAGENTA}Started generating!\nctrl+c to exit process!\n{Style.RESET_ALL}")
                                    generator.startGenerating(args)
                                    break
                                elif b.lower() == "n":
                                    clear()
                                    runMain()
                                    break
                            break
        elif choice == "5":
            webbrowser.open("https://discord.gg/QbcrQkHFzB", 1)
            clear()
            runMain()
        elif choice == "6":
            clear()
            print(f"{Fore.RED}Exitting application...")
            sleep(1)
            clear()
            os._exit(0)
        else:
            clear()
            runMain()
    runMain()
except KeyboardInterrupt:
    print(f"\n{Fore.RED}User interrupted application...")
    os._exit(0)
