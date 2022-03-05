import json
from plugins.util import *

class Args:
    def __init__(self, model_:str, prompts_:str, width_:str, height_:str, interval_image_:str, seed_:str, max_iterations_:str, slot_:str):
        self.model = str(model_)
        self.prompts = str(prompts_)
        self.width = str(width_)
        self.height = str(height_)
        self.interval_image = str(interval_image_)
        self.seed = str(seed_)
        self.max_iterations = str(max_iterations_)
        self.slot = str(slot_)
    
    def getAll(self):
        return f"{Style.RESET_ALL}Slot: {self.slot}\nModel: {self.model}\nPrompts: {self.prompts}\nWidth: {self.width}\nHeight: {self.height}\nSeed: {self.seed}\nMax Iteration: {self.max_iterations}"