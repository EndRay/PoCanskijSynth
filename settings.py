import os.path

SAMPLERATE = 44100

SRC_FOLDER = os.path.abspath(os.path.join("realisations", "cpp"))

PATH_TO_GENERATED = os.path.abspath("tmp/generated")
GENERATED_CPP = os.path.join(PATH_TO_GENERATED, "cpp")

PATH_TO_CPP = os.path.abspath("cpp")
TEMPLATES_FOLDER = os.path.join(PATH_TO_CPP, "templates")

FOLDER_TO_COMPILE = os.path.abspath("tmp/to_compile")
RESULTS_FOLDER = os.path.abspath("results")

EMPTY_BLOCK_COMMENTS = True
