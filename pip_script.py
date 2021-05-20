from sys import platform, executable, argv
from pathlib import Path
import os
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--noedit", action='store_true', help="Installer en mode éditable")
    parser.add_argument("--nodev", action='store_true', help="Installer sans les dépendances de développement")
    parser.add_argument("--notest", action='store_true', help="Installer sans les dépendances de test")
    args = parser.parse_args()
    editable = "-e" if not args.noedit else ""
    test = "test" if not args.notest else ""
    dev = "dev" if not args.nodev else ""
    path = Path(argv[0]).absolute().parent

    arg_extras = "[" if test != "" or dev != "" else ""
    arg_extras += test
    arg_extras += "," if test != "" and dev != "" else ""
    arg_extras += dev
    arg_extras += "]" if test != "" or dev != "" else ""
    
    python_exec = Path(executable)
    python_exec = f"{python_exec.stem}{python_exec.suffix}"

    if not Path(".venv").exists():
        os.system(f"{python_exec} -m pip install -U pip setuptools")
        os.system(f"{python_exec} -m venv .venv")

    if platform == 'win32':
        python_venv_exec = str(Path(f".venv/Scripts/{python_exec}"))
    else:
        python_venv_exec = str(Path(f".venv/bin/{python_exec}"))

    os.system(f"{python_venv_exec} -m pip install -U pip setuptools wheel")
    os.system(f"{python_venv_exec} -m pip install {editable} {path}{arg_extras}")
    os.system(f"{python_venv_exec} -m pip uninstall -y wheel")
