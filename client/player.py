import subprocess
import sys
import os

def open_file(path: str):
    if sys.platform.startswith('win'):
        os.startfile(path)
    elif sys.platform.startswith('darwin'):
        subprocess.run(['open', path])
    else:
        subprocess.run(['xdg-open', path])