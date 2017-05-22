import docopt
import os
import sys
import subprocess
from . import environment as env
from .gitutils import clone

if __name__ == "__main__":
    if not os.path.exists(env.CMAKE_SCRIPTS):
        clone(env.CMAKE_SCRIPTS_URL, env.CMAKE_SCRIPTS)
    
    if len(sys.argv) == 1:
        toolchains = os.listdir(env.TOOLCHAINS_DIR)
        print toolchains
    else:
        toolchain = os.path.join(env.TOOLCHAINS_DIR, sys.argv[1] + ".cmake")
        try:
          os.makedirs("build")
        except OSError:
            pass

        cwd = os.getcwd()
        os.chdir("build")
        subprocess.call(["cmake",
            "-DCMAKE_TOOLCHAIN_FILE=" + toolchain,
            "-DCMAKE_BUILD_TYPE=Release",
            ".."])
        os.chdir(cwd)

