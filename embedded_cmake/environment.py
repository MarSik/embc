import os

HOME=os.path.expanduser('~')
EMBC=os.path.join(HOME, ".embc")
CWD=os.getcwd()

PACKAGES_DIR = os.path.join(EMBC, "packages")
CMAKE_ROOT = os.path.join(EMBC, "cmake")

CMAKE_SCRIPTS_SUBDIR=".embc/scripts"
CMAKE_SCRIPTS=os.path.join(CWD, CMAKE_SCRIPTS_SUBDIR)
CMAKE_SCRIPTS_URL="https://MarSik@bitbucket.org/MarSik/embedded-cmake.git"

TOOLCHAINS_DIR = os.path.join(CMAKE_SCRIPTS, "Toolchains")
TEMPLATE_DIR = os.path.join(CMAKE_SCRIPTS, "Templates")
TEMPLATE_SUFFIX = ".j2"

CMAKE_PACKAGE = "https://github.com/Kitware/CMake/releases/download/v3.14.0-rc2/cmake-3.14.0-rc2-Linux-x86_64.tar.gz"

PROJECT_LIB = "lib"
