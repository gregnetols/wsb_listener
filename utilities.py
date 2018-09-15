'''
general utilities
'''
import yaml

def read_yml(File):
    with open(File, 'r') as f:
        yaml_file = yaml.load(f)
    return yaml_file
