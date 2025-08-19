#!/usr/bin/python3

import argparse
import logging
import os
from pathlib import Path
import platform
from pprint import pprint
import shutil
import socket
import subprocess
from subprocess import PIPE
import sys

from module.args import parse_args
from module.fetch import patch, validate_and_download
from module.path import ProjectPaths
from module.profile import BranchProfile, resolve_profile
from module.util import MINGW_ARCH_2_XMAKE_ARCH_MAP, ensure

def clean(config: argparse.Namespace, paths: ProjectPaths):
  if paths.test_dir.exists():
    shutil.rmtree(paths.test_dir)

def prepare_dirs(paths: ProjectPaths):
  paths.pkg_dir.mkdir(parents = True, exist_ok = True)
  shutil.copytree(
    paths.test_src_dir,
    paths.test_dir,
    ignore = shutil.ignore_patterns(
      '.cache',
      '.vscode',
      '.xmake',
      'build',
    ),
  )

def extract(path: Path, arx: Path):
  ensure(path.parent)
  subprocess.run([
    'bsdtar',
    '-C', path.parent,
    '-xf', arx,
    '--no-same-owner',
  ], check = True)

def fetch_xmake(ver: BranchProfile, paths: ProjectPaths):
  paths.assets_dir.mkdir(parents = True, exist_ok = True)
  xmake_url = f'https://github.com/xmake-io/xmake/releases/download/v{ver.xmake}/{paths.test_xmake_pkg.name}'
  validate_and_download(paths.test_xmake_pkg, xmake_url)

def winepath(path: Path) -> str:
  if platform.system() == 'Windows':
    return str(path)
  else:
    return subprocess.check_output(['winepath', '-w', path]).decode().strip()

def prepend_to_path_string(path: Path, path_string: str) -> str:
  if not path_string:
    return winepath(path)
  return winepath(path) + ';' + path_string

def prepend_to_path(path: Path):
  if platform.system() == 'Windows':
    os.environ['PATH'] = prepend_to_path_string(path, os.getenv('PATH'))
  else:
    os.environ['WINEPATH'] = prepend_to_path_string(path, os.getenv('WINEPATH'))

def prepare_test_binary(ver: BranchProfile, paths: ProjectPaths):
  extract(paths.test_mingw_dir, paths.mingw_pkg)
  prepend_to_path(paths.test_mingw_dir / 'bin')

  fetch_xmake(ver, paths)
  extract(paths.test_xmake_dir, paths.test_xmake_pkg)
  paths.test_xmake_exe.chmod(0o755)

  extract(paths.pkg_dir, paths.library_pkg)
  for key, value in paths.pkg._asdict().items():
    if value.name.endswith('.tar'):
      extract(paths.test_mingw_dir / 'lib', value)

def test_library(ver: BranchProfile, paths: ProjectPaths, verbose: list[str]):
  xmake = paths.test_xmake_exe
  subprocess.check_call([
    xmake, 'f', *verbose,
    '-p', 'mingw', '-a', MINGW_ARCH_2_XMAKE_ARCH_MAP[ver.arch],
    f'--mingw={winepath(paths.test_mingw_dir)}',
  ], cwd = paths.test_dir)
  subprocess.check_call([xmake, 'b', *verbose], cwd = paths.test_dir)
  subprocess.check_call([xmake, 'test', *verbose], cwd = paths.test_dir)

def main():
  config = parse_args()

  if config.verbose >= 2:
    logging.basicConfig(level = logging.DEBUG)
    os.environ['WINEDEBUG'] = ''
    xmake_verbose = ['-vD']
  elif config.verbose >= 1:
    logging.basicConfig(level = logging.INFO)
    os.environ['WINEDEBUG'] = 'fixme-all'
    xmake_verbose = ['-v']
  else:
    logging.basicConfig(level = logging.ERROR)
    os.environ['WINEDEBUG'] = '-all'
    xmake_verbose = []

  logging.info("testing library %s with mingw%s-%s", config.branch, config.profile, config.mingw_lite_version)

  ver = resolve_profile(config)
  paths = ProjectPaths(config, ver)

  clean(config, paths)

  prepare_dirs(paths)

  prepare_test_binary(ver, paths)

  test_report = {
    'fail': False,
  }

  try:
    test_library(ver, paths, xmake_verbose)
    test_report['mingw64-compiler'] = "okay"
  except Exception as e:
    test_report['fail'] = True
    test_report['mingw64-compiler'] = repr(e)

  print("============================== TEST REPORT ==============================")
  pprint(test_report)

  if test_report['fail']:
    sys.exit(1)

if __name__ == '__main__':
  main()
