import subprocess, os
from utilities import definitions


class Map_Selector_Window():
    def __init__(self):
        file_path = os.path.join(definitions.PROGRAM_ROOT, "maps")
        subprocess.Popen(f'explorer "{file_path}"')
