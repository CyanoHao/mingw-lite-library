#!/usr/bin/python3

import argparse
from pathlib import Path
import shutil
import subprocess
from subprocess import Popen, PIPE

from module.args import parse_args
from module.path import ProjectPaths
from module.prepare_source import prepare_source
from module.profile import BranchProfile, resolve_profile

from module.AAB import build_AAB_library

def clean(config: argparse.Namespace, paths: ProjectPaths):
  if paths.build_dir.exists():
    shutil.rmtree(paths.build_dir)
  if paths.layer_dir.exists():
    shutil.rmtree(paths.layer_dir)
  if paths.pkg_dir.exists():
    shutil.rmtree(paths.pkg_dir)

def prepare_dirs(paths: ProjectPaths):
  paths.assets_dir.mkdir(parents = True, exist_ok = True)
  paths.build_dir.mkdir(parents = True, exist_ok = True)
  paths.pkg_dir.mkdir(parents = True, exist_ok = True)
  paths.dist_dir.mkdir(parents = True, exist_ok = True)

def extract(path: Path, arx: Path):
  subprocess.run([
    'bsdtar',
    '-C', path.parent,
    '-xf', arx,
    '--no-same-owner',
  ], check = True)

def prepare_test_binary(ver: BranchProfile, paths: ProjectPaths):
  extract(paths.toolchain.prefix, paths.cross_pkg)

def package(src: Path, dst: Path):
  tar = Popen([
    'bsdtar', '-c',
    '-C', src.parent,
    '--numeric-owner',
    src.name,
  ], stdout = PIPE)
  zstd = Popen([
    'zstd', '-f',
    '--zstd=strat=5,wlog=27,hlog=25,slog=6,ovlog=9',
    '-o', dst,
  ], stdin = tar.stdout)
  tar.stdout.close()
  zstd.communicate()
  tar.wait()
  if tar.returncode != 0 or zstd.returncode != 0:
    raise Exception('bsdtar | zstd failed')

def main():
  config = parse_args()

  ver = resolve_profile(config)
  paths = ProjectPaths(config, ver)

  if config.clean:
    clean(config, paths)

  prepare_dirs(paths)

  prepare_source(ver, paths, config.download_only)

  if config.download_only:
    return

  prepare_test_binary(ver, paths)

  build_AAB_library(ver, paths, config)

  package(paths.pkg_dir, paths.library_pkg)

if __name__ == '__main__':
  main()
