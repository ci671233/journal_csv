OPENAI_KEY = "Chat Bot KEY"
INPUT_PATH = "./input"
OUTPUT_PATH = "./output"


import os
if os.path.isfile("./instance/config.py"):
    from instance.config import *