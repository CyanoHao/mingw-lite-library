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

def cflags(
  mingw_arch: str,
  cpp_extra: List[str] = [],
  common_extra: List[str] = [],
  ld_extra: List[str] = [],
  c_extra: List[str] = [],
  cxx_extra: List[str] = [],
  optimize_for_size: bool = False,
  lto: bool = False,
) -> List[str]:
  triplet = MINGW_ARCH_2_TRIPLET_MAP[mingw_arch]
  cpp = ['-DNDEBUG']
  common = ['-pipe']
  ld = ['-s']
  if lto:
    # lto does not work with -Os
    common.extend(['-O2', '-flto'])
    ld.extend(['-O2', '-flto'])
  else:
    if optimize_for_size:
      common.append('-Os')
    else:
      common.append('-O2')
  return [
    f'CC={triplet}-gcc',
    f'CXX={triplet}-g++',
    f'AR={triplet}-gcc-ar',
    f'RANLIB={triplet}-gcc-ranlib',
    'CPPFLAGS=' + ' '.join(cpp + cpp_extra),
    'CFLAGS=' + ' '.join(common + common_extra + c_extra),
    'CXXFLAGS=' + ' '.join(common + common_extra + cxx_extra),
    'LDFLAGS=' + ' '.join(ld + ld_extra),
  ]

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

def configure(cwd: Path, args: List[str]):
  subprocess.run(
    ['../configure', *args],
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

def make_default(cwd: Path, jobs: int):
  make_custom(cwd, [], jobs)

def make_destdir_install(cwd: Path, destdir: Path):
  make_custom(cwd, [f'DESTDIR={destdir}', 'install'], jobs = 1)

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

def pkgconfig_add_missing(
  pkgconfig_file: Path,
  libs: List[str] = [],
  libs_private: List[str] = [],
  requires: List[str] = [],
  requires_private: List[str] = [],
):
  with open(pkgconfig_file, 'r') as f:
    pkgconfig = f.readlines()
  new_pkgconfig = []
  new_libs = []
  new_libs_private = []
  new_requires = []
  new_requires_private = []
  for line in pkgconfig:
    if line.startswith('Libs:'):
      new_libs = line.split()[1:]
    elif line.startswith('Libs.private:'):
      new_libs_private = line.split()[1:]
    elif line.startswith('Requires:'):
      new_requires = line.split()[1:]
    elif line.startswith('Requires.private:'):
      new_requires_private = line.split()[1:]
    else:
      new_pkgconfig.append(line)

  for lib in libs:
    if lib not in new_libs:
      new_libs.append(lib)
  for lib in libs_private:
    if lib not in new_libs_private:
      new_libs_private.append(lib)
  for req in requires:
    if req not in new_requires:
      new_requires.append(req)
  for req in requires_private:
    if req not in new_requires_private:
      new_requires_private.append(req)

  if new_libs:
    pkgconfig.append('Libs: ' + ' '.join(new_libs) + '\n')
  if new_libs_private:
    pkgconfig.append('Libs.private: ' + ' '.join(new_libs_private) + '\n')
  if new_requires:
    pkgconfig.append('Requires: ' + ' '.join(new_requires) + '\n')
  if new_requires_private:
    pkgconfig.append('Requires.private: ' + ' '.join(new_requires_private) + '\n')

  with open(pkgconfig_file, 'w') as f:
    f.writelines(pkgconfig)
