import os

HOME=os.path.expanduser('~')
EMBC=os.path.join(HOME, ".embc")

CMAKE_SCRIPTS=os.path.join(EMBC, "scripts")
CMAKE_SCRIPTS_URL="https://MarSik@bitbucket.org/MarSik/embedded-cmake.git"

TOOLCHAINS_DIR = os.path.join(CMAKE_SCRIPTS, "Toolchains")

