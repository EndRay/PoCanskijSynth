import os
from distutils.dir_util import copy_tree

from settings import GENERATED_CPP, PATH_TO_CPP, FOLDER_TO_COMPILE


def collect_files():
    # copy all files from folder cpp/src/ to tmp/
    copy_tree(os.path.join(PATH_TO_CPP, "src"), FOLDER_TO_COMPILE)
    # copy all files from folder generated/cpp/ to tmp/
    copy_tree(GENERATED_CPP, FOLDER_TO_COMPILE)