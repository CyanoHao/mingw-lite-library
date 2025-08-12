from contextlib import contextmanager
import logging
from pathlib import Path
import re
import subprocess
from typing import Iterable, List

MINGW_ARCH_2_CMAKE_PROCESSOR_MAP = {
  '64': 'AMD64',
  'arm64': 'ARM64',
  '32': 'x86',
}

MINGW_ARCH_2_TRIPLET_MAP = {
  '64': 'x86_64-w64-mingw32',
  'arm64': 'aarch64-w64-mingw32',
  '32': 'i686-w64-mingw32',
}

MINGW_ARCH_2_XMAKE_ARCH_MAP = {
  '64': 'x86_64',
  'arm64': 'aarch64',
  '32': 'i686',
}

def cmake_build(
  cwd: Path,
  jobs: int,
  build_dir: str = 'build',
):
  subprocess.run(
    ['cmake', '--build', build_dir, '--parallel', str(jobs)],
    cwd = cwd,
    check = True,
  )

def cmake_config(
  cwd: Path,
  extra_args: List[str],
  build_dir: str = 'build',
):
  subprocess.run(
    ['cmake', '-S', '.', '-B', build_dir, *extra_args],
    cwd = cwd,
    check = True,
  )

def cmake_flags(
  mingw_arch: str,
  optimize_for_size: bool = False,
  lto: bool = False,
) -> List[str]:
  cmake_processor = MINGW_ARCH_2_CMAKE_PROCESSOR_MAP[mingw_arch]
  triplet = MINGW_ARCH_2_TRIPLET_MAP[mingw_arch]
  build_type = ''
  lto_flag = []

  if optimize_for_size:
    build_type = 'MinSizeRel'
  else:
    build_type = 'Release'
  if lto:
    lto_flag = ['-DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON']

  return [
    f'-DCMAKE_SYSTEM_NAME=Windows',
    f'-DCMAKE_SYSTEM_PROCESSOR={cmake_processor}',
    f'-DCMAKE_C_COMPILER={triplet}-gcc',
    f'-DCMAKE_CXX_COMPILER={triplet}-g++',
    f'-DCMAKE_AR:FILEPATH={triplet}-gcc-ar',
    f'-DCMAKE_RANLIB:FILEPATH={triplet}-gcc-ranlib',
    f'-DCMAKE_BUILD_TYPE={build_type}',
    *lto_flag,
  ]

def cmake_install(
  cwd: Path,
  destdir: Path,
  targets: List[str] = [],
  build_dir: str = 'build',
):
  subprocess.run(
    ['cmake', '--install', build_dir, '--prefix', destdir, *targets],
    cwd = cwd,
    check = True,
  )

def ensure(path: Path):
  path.mkdir(parents = True, exist_ok = True)

def make_custom(cwd: Path, extra_args: List[str], jobs: int):
  subprocess.run(
    ['make', '-j', str(jobs), *extra_args],
    cwd = cwd,
    check = True,
  )

@contextmanager
def overlayfs_ro(merged: Path | str, lower: list[Path]):
  try:
    if len(lower) == 1:
      subprocess.run([
        'mount',
        '--bind',
        lower[0],
        merged,
        '-o', 'ro',
      ])
    else:
      lowerdir = ':'.join(map(str, lower))
      subprocess.run([
        'mount',
        '-t', 'overlay',
        'none',
        merged,
        '-o', f'lowerdir={lowerdir}',
      ], check = True)
    yield
  finally:
    subprocess.run(['umount', merged])

def package(root: Path, dst: Path):
  subprocess.run([
    'bsdtar', '-c',
    '-C', root,
    '-f', dst,
    '--numeric-owner',
    '.',
  ], check = True)
