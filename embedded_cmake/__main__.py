"""
Usage:
  embc list
  embc init <toolchain> [--cpu=<cpu>] [-f=<frequency>]
  embc build [--verbose]
  embc update
  embc -h | --help
  embc --version

Options:
  -h --help       Show this help
  --version       Show project version
  --cpu=<cpu>     Override the default CPU type
  -f=<frequency>  Override the default CPU frequency
  --verbose       Be verbose during build
"""

from __future__ import print_function
import docopt
import os

import subprocess
from jinja2 import Template

from . import environment as env
from .gitutils import clone, update


def install_embedded_cmake():
    if not os.path.exists(env.CMAKE_SCRIPTS):
        clone(env.CMAKE_SCRIPTS_URL, env.CMAKE_SCRIPTS)

def update_embedded_cmake():
    install_embedded_cmake()
    update(env.CMAKE_SCRIPTS)

def toolchain_info(filename):
    with open(os.path.join(env.TOOLCHAINS_DIR, filename)) as f:
        header = f.readline()
    name = os.path.basename(filename).replace(".cmake", "")
    if not header.startswith("#"):
        header = ""
    return name + "\t\t" + header.lstrip("# \t")

def prepare_template(filename, toolchain_name, *args, **kwargs):
    if not os.path.exists(filename):
        template_file = os.path.join(env.TEMPLATE_DIR, toolchain_name, filename)
        if os.path.exists(template_file):
            print("Preparing default " + filename)
            with open(filename, "w") as dest, open(template_file) as tpl:
                template = Template(tpl.read())
                dest.write(template.render(*args, **kwargs))
        else:
            print(filename + " template for " + toolchain_name +
                  " not found. Please create it manually")
    else:
        print("Keeping the existing " + filename + " intact")


if __name__ == "__main__":
    options = docopt.docopt(__doc__, version = "0.1")
    print(options)

    if len(options) == 0:
        print(__doc__)
        exit(1)

    if options["update"]:
        update_embedded_cmake()
        exit(0)

    if options["list"]:
        install_embedded_cmake()
        toolchains = os.listdir(env.TOOLCHAINS_DIR)
        [ print(toolchain_info(toolchain))
          for toolchain in sorted(toolchains)
          if toolchain.endswith(".cmake") ]
        exit(0)

    if options["build"]:
        makecmd = ["make"]
        if options["--verbose"]:
            makecmd.append("VERBOSE=1")

        for f in os.listdir("."):
            if os.path.isdir(f) and f.startswith("build-"):
                cwd = os.getcwd()
                os.chdir(f)
                print("--- Building {toolchain} ---".format(toolchain = f[6:]))
                rc = subprocess.Popen(makecmd).wait()
                os.chdir(cwd)
                if rc != 0:
                    exit(1)
        exit(0)

    if options["init"]:
        install_embedded_cmake()
        toolchain_name = options["<toolchain>"]
        toolchain = os.path.join(env.TOOLCHAINS_DIR, toolchain_name + ".cmake")

        if not os.path.exists(toolchain):
            print("The requested toolchain " + toolchain_name + " does not exist.")
            exit(1)

        # Prepare template CMakefile
        for tpl in os.listdir(os.path.join(env.TEMPLATE_DIR, toolchain_name)):
            prepare_template(tpl,
                             toolchain_name,
                             CPU = options["--cpu"],
                             F_CPU = options["-f"])

        # Create build directory
        try:
          os.makedirs("build-" + toolchain_name)
        except OSError:
            pass

        cwd = os.getcwd()
        os.chdir("build-" + toolchain_name)

        new_env = {}
        new_env.update(os.environ)
        new_env["TOOLCHAIN_ROOT"] = env.PACKAGES_DIR

        subprocess.Popen(["cmake",
                          "--no-warn-unused-cli",
                          "-Wno-dev",
                          "-DDOWNLOAD_DEPENDENCIES=1",
                          "-DCMAKE_PREFIX_PATH=" + env.PACKAGES_DIR,
                          "-DDOWNLOAD_DIR=" + env.PACKAGES_DIR,
                          "-DCMAKE_TOOLCHAIN_FILE=" + toolchain,
                          "-DCMAKE_BUILD_TYPE=Release",
                          ".."],
                         env = new_env).wait()
        os.chdir(cwd)
        exit(0)

