'''
general utilities
'''
import yaml

def read_yml(File):
    '''
    '''
    with open(File, 'r') as f:
        yaml_file = yaml.load(f)
    return yaml_file


def new_hour(current_hour):
    if current_hour not datetime.now().hour:
        return True
    else return False

def new_dat(current_day):
    if current_day not datetime.now().day:
        return True
    else return False
