import os

VERSION = '0.0.0.0'


def get_project_root():
    return os.path.dirname(os.path.dirname(__file__))
#

def get_library_root():
    return os.path.dirname(__file__)
#
