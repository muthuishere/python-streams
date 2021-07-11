from pathlib import Path


def get_current_path():
    return  str(Path(__file__).parent.absolute())



def getfemale_babies_file_name():
    return get_current_path() + '\\resources\\female_babies.txt'

def create_output_file(filename):
    return get_current_path() + '\\output\\' +filename

def get_file_contents(filename):
    txt = Path(filename).read_text()
    return txt

def file_exists(filename):
    return Path(filename).exists()

