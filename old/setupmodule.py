from plugins.util import *
from plugins.model import Model
from plugins.choice import printAllChoice
import sys
sys.path.append("./")
import main as mainscript
from tqdm.auto import tqdm
import os
import requests
import shutil
import subprocess as sub


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
            if choiceInt < len(models)+1:
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
        sub.call("git clone https://github.com/openai/CLIP ./scripts/CLIP".split(' '))
        
        print(f"{yellow}Downloading VQGAN..{Style.RESET_ALL}.")
        sub.call("git clone https://github.com/CompVis/taming-transformers ./scripts/taming-transformers".split(' '))

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
        sub.call("pip install -r ./scripts/requirements.txt".split(' '))
        a = "python3"
        if getPlatform() == "win": a="py"
        sub.call(f"{a} -m pip install --upgrade pillow".split(' '))

        print(f"{yellow}Downloading exempi...{Style.RESET_ALL}")
        sub.call("brew install exempi".split(' '))

        print(f"{Fore.LIGHTGREEN_EX}Successfully completed process!")
        os._exit(0)
    except Exception as e:
        print(red+e)
        print(f"{red}An error occured...")
        os._exit(0)

def fuckyoumfpython():
    print(f"{Fore.YELLOW}Loading...")
    wait(0.5)
    setConsoleSize(23, 72)
    wait(1)
    while True:
        clear()
        print(setupLogo)
        print('')
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
            mainscript.run()
            break
