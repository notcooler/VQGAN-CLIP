from sys import platform
from time import sleep
from colorama import Fore, Back, Style
from plugins.model import Model
import os
import sys

skip = False
startBanner = f"""{Fore.BLUE}██╗░░░██╗░██████╗░░██████╗░░█████╗░███╗░░██╗░░░░░░░░█████╗░██╗░░░░░██╗██████╗░
██║░░░██║██╔═══██╗██╔════╝░██╔══██╗████╗░██║░░██╗░░██╔══██╗██║░░░░░██║██╔══██╗
╚██╗░██╔╝██║██╗██║██║░░██╗░███████║██╔██╗██║██████╗██║░░╚═╝██║░░░░░██║██████╔╝
░╚████╔╝░╚██████╔╝██║░░╚██╗██╔══██║██║╚████║╚═██╔═╝██║░░██╗██║░░░░░██║██╔═══╝░
░░╚██╔╝░░░╚═██╔═╝░╚██████╔╝██║░░██║██║░╚███║░░╚═╝░░╚█████╔╝███████╗██║██║░░░░░
░░░╚═╝░░░░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝░░░░░░░░╚════╝░╚══════╝╚═╝╚═╝░░░░░{Fore.YELLOW}
NOTE: Original code comes from a collab!
This is made so you can run it easily on your own computer!
{Fore.CYAN}Made by: Cooler#8190"""
logo = f"""{Fore.BLUE}██╗░░░██╗░██████╗░░██████╗░░█████╗░███╗░░██╗░░░░░░░░█████╗░██╗░░░░░██╗██████╗░
██║░░░██║██╔═══██╗██╔════╝░██╔══██╗████╗░██║░░██╗░░██╔══██╗██║░░░░░██║██╔══██╗
╚██╗░██╔╝██║██╗██║██║░░██╗░███████║██╔██╗██║██████╗██║░░╚═╝██║░░░░░██║██████╔╝
░╚████╔╝░╚██████╔╝██║░░╚██╗██╔══██║██║╚████║╚═██╔═╝██║░░██╗██║░░░░░██║██╔═══╝░
░░╚██╔╝░░░╚═██╔═╝░╚██████╔╝██║░░██║██║░╚███║░░╚═╝░░╚█████╔╝███████╗██║██║░░░░░
░░░╚═╝░░░░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝░░░░░░░░╚════╝░╚══════╝╚═╝╚═╝░░░░░"""

setupLogo = f"""{Fore.CYAN}░░██╗░░██╗░░██╗░██████╗███████╗████████╗██╗░░░██╗██████╗░██╗░░██╗░░██╗░░
░██╔╝░██╔╝░██╔╝██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗╚██╗░╚██╗░╚██╗░
██╔╝░██╔╝░██╔╝░╚█████╗░█████╗░░░░░██║░░░██║░░░██║██████╔╝░╚██╗░╚██╗░╚██╗
╚██╗░╚██╗░╚██╗░░╚═══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔═══╝░░██╔╝░██╔╝░██╔╝
░╚██╗░╚██╗░╚██╗██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░██╔╝░██╔╝░██╔╝░
░░╚═╝░░╚═╝░░╚═╝╚═════╝░╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░░░╚═╝░░╚═╝░░╚═╝░░"""

slotsLogo = f"""{Fore.MAGENTA}███████╗██████╗░██╗████████╗░░░██████╗██╗░░░░░░█████╗░████████╗░██████╗
██╔════╝██╔══██╗██║╚══██╔══╝░░██╔════╝██║░░░░░██╔══██╗╚══██╔══╝██╔════╝
█████╗░░██║░░██║██║░░░██║░░░░░╚█████╗░██║░░░░░██║░░██║░░░██║░░░╚█████╗░
██╔══╝░░██║░░██║██║░░░██║░░░░░░╚═══██╗██║░░░░░██║░░██║░░░██║░░░░╚═══██╗
███████╗██████╔╝██║░░░██║░░░░░██████╔╝███████╗╚█████╔╝░░░██║░░░██████╔╝
╚══════╝╚═════╝░╚═╝░░░╚═╝░░░░░╚═════╝░╚══════╝░╚════╝░░░░╚═╝░░░╚═════╝░"""

models = [
    Model("vqgan_imagenet_f16_1024", "https://heibox.uni-heidelberg.de/d/8088892a516d4e3baf92/files/?p=%2Fconfigs%2Fmodel.yaml&dl=1", "https://heibox.uni-heidelberg.de/d/8088892a516d4e3baf92/files/?p=%2Fckpts%2Flast.ckpt&dl=1"),
    Model("vqgan_imagenet_f16_16384", "https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fconfigs%2Fmodel.yaml&dl=1", "https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fckpts%2Flast.ckpt&dl=1"),
    Model("gumbel_8192", "https://heibox.uni-heidelberg.de/d/2e5662443a6b4307b470/files/?p=%2Fconfigs%2Fmodel.yaml&dl=1", "https://heibox.uni-heidelberg.de/d/2e5662443a6b4307b470/files/?p=%2Fckpts%2Flast.ckpt&dl=1"),
    Model("coco", "https://dl.nmkd.de/ai/clip/coco/coco.yaml", "https://dl.nmkd.de/ai/clip/coco/coco.ckpt"),
    Model("faceshq", "https://drive.google.com/uc?export=download&id=1fHwGx_hnBtC8nsq7hesJvs-Klv-P0gzT", "https://app.koofr.net/content/links/a04deec9-0c59-4673-8b37-3d696fe63a5d/files/get/last.ckpt?path=%2F2020-11-13T21-41-45_faceshq_transformer%2Fcheckpoints%2Flast.ckpt"),
    Model("wikiart_1024", "http://mirror.io.community/blob/vqgan/wikiart.yaml", "http://mirror.io.community/blob/vqgan/wikiart.ckpt"),
    Model("wikiart_16384", "http://eaidata.bmk.sh/data/Wikiart_16384/wikiart_f16_16384_8145600.yaml", "http://eaidata.bmk.sh/data/Wikiart_16384/wikiart_f16_16384_8145600.ckpt"),
    Model("sflckr", "https://heibox.uni-heidelberg.de/d/73487ab6e5314cb5adba/files/?p=%2Fconfigs%2F2020-11-09T13-31-51-project.yaml&dl=1", "https://heibox.uni-heidelberg.de/d/73487ab6e5314cb5adba/files/?p=%2Fcheckpoints%2Flast.ckpt&dl=1"),
    Model("ade20k", "https://static.miraheze.org/intercriaturaswiki/b/bf/Ade20k.txt", "https://app.koofr.net/content/links/0f65c2cd-7102-4550-a2bd-07fd383aac9e/files/get/last.ckpt?path=%2F2020-11-20T21-45-44_ade20k_transformer%2Fcheckpoints%2Flast.ckpt"),
    Model("ffhq", "https://app.koofr.net/content/links/0fc005bf-3dca-4079-9d40-cdf38d42cd7a/files/get/2021-04-23T18-19-01-project.yaml?path=%2F2021-04-23T18-19-01_ffhq_transformer%2Fconfigs%2F2021-04-23T18-19-01-project.yaml&force", "https://app.koofr.net/content/links/0fc005bf-3dca-4079-9d40-cdf38d42cd7a/files/get/last.ckpt?path=%2F2021-04-23T18-19-01_ffhq_transformer%2Fcheckpoints%2Flast.ckpt&force"),
    Model("celebahq", "https://app.koofr.net/content/links/6dddf083-40c8-470a-9360-a9dab2a94e96/files/get/2021-04-23T18-11-19-project.yaml?path=%2F2021-04-23T18-11-19_celebahq_transformer%2Fconfigs%2F2021-04-23T18-11-19-project.yaml&force", "https://app.koofr.net/content/links/6dddf083-40c8-470a-9360-a9dab2a94e96/files/get/last.ckpt?path=%2F2021-04-23T18-11-19_celebahq_transformer%2Fcheckpoints%2Flast.ckpt&force")
]

def getPlatform():
    plt = "unknown"
    if platform == "linux" or platform == "linux2":
        plt = "lin"
    elif platform == "win32":
        plt = "win"
    elif platform == "darwin":
        plt = "mac"
    return plt

def clear():
    if getPlatform() == "win":
        os.system('cls')
    elif getPlatform() == "lin" or getPlatform() == "mac":
        os.system('clear')
    else:
        pass

def setConsoleSize(*_x, **_y):
    x = '23'
    y = '78'
    if _x != None and len(_x) != 0: x = str(_x[0])
    if _y != None and len(_x) != 0: y = str(_x[1])
    if getPlatform() == "win":
        os.system(f'mode {x},{y}')
    elif getPlatform() == "lin" or getPlatform() == "mac":
        os.system(f'resize -s {x} {y}')
    else:
        pass

def printPerChar(msg:str=None):
    if msg != None and msg != "":
        for char in msg:
            sleep(0.05)
            sys.stdout.write(char)
            sys.stdout.flush()
        print("")

def wait(seconds:int=None):
    if seconds != None and skip == False: sleep(seconds)
