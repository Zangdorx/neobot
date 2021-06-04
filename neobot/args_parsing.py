from __future__ import annotations

import argparse
from argparse import Namespace


class MissingArgumentsError(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise MissingArgumentsError(message)
