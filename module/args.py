import argparse
import logging
import os
import subprocess
from subprocess import PIPE

from module.profile import BRANCHES

def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-b', '--branch',
    type = str,
    choices = BRANCHES.keys(),
    required = True,
    help = 'MinGW Lite Library branch to build',
  )
  parser.add_argument(
    '-p', '--profile',
    type = str,
    required = True,
    help = 'MinGW Lite profile',
  )
  parser.add_argument(
    '-mv', '--mingw-lite-version',
    type = str,
    required = True,
    help = 'MinGW Lite version',
  )

  parser.add_argument(
    '-c', '--clean',
    action = 'store_true',
    help = 'Clean build directories',
  )
  parser.add_argument(
    '-j', '--jobs',
    type = int,
    default = os.cpu_count(),
  )
  parser.add_argument(
    '--download-only',
    action = 'store_true',
    help = 'Download sources only',
  )
  parser.add_argument(
    '-v', '--verbose',
    action = 'count',
    default = 0,
    help = 'Increase verbosity (up to 2)',
  )

  result = parser.parse_args()
  return result
