import subprocess

class Map_Selector_Window():
    def __init__(self,PROGRAM_ROOT):
        file_path = PROGRAM_ROOT + "\maps\\"
        subprocess.Popen(f'explorer "{file_path}"')
        