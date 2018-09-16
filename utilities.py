'''
general utilities
'''
import yaml
from datetime import datetime

def read_yml(File):
    '''
    '''
    with open(File, 'r') as f:
        yaml_file = yaml.load(f)
    return yaml_file


def new_hour(current_hour):
    print(current_hour, '----', datetime.now().hour, '----', datetime.now())
    if current_hour != datetime.now().hour:
        print('Entered branch')
        return True
    else:
        return False


def new_day(current_day):
    if current_day != datetime.now().day:
        return True
    else:
        return False
