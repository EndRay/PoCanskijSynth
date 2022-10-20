import os

from settings import FOLDER_TO_COMPILE


def compile_cpp(exe_name, cpp_name):
    exe_name += ".exe"
    os.system(
        f"g++ "
        f"{os.path.join(FOLDER_TO_COMPILE, cpp_name)} "
        f"-o {os.path.join(FOLDER_TO_COMPILE, exe_name)} "
        f"-std=c++17 -w")

