import argparse
import os
import shutil

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchProfile
from module.util import cmake_build, cmake_config, cmake_flags, cmake_install, ensure, make_custom, overlayfs_ro, package, MINGW_ARCH_2_TRIPLET_MAP

def onetbb(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  with overlayfs_ro('/usr/local', [
    paths.toolchain.binutils / 'usr/local',
    paths.toolchain.crt / 'usr/local',
    paths.toolchain.gcc / 'usr/local',
    paths.toolchain.headers / 'usr/local',
  ]):
    cmake_config(paths.src_dir.onetbb, [
      '-DBUILD_SHARED_LIBS=OFF',
      '-DTBB_TEST=OFF',
      '-DTBB_STRICT=OFF',
      *cmake_flags(ver.arch, ver.optimize_for_size),
    ])
    cmake_build(paths.src_dir.onetbb, config.jobs)
    cmake_install(paths.src_dir.onetbb, paths.layer.onetbb)

    # allow link with `-ltbb` as documented by libstdc++
    versioned = paths.layer.onetbb / 'lib/libtbb12.a'
    unversioned = paths.layer.onetbb / 'lib/libtbb.a'
    if unversioned.exists():
      if not versioned.samefile(unversioned):
        unversioned.unlink()
        os.link(versioned, unversioned)
    else:
      os.link(versioned, unversioned)

    ensure(paths.layer.onetbb / 'share/licenses/onetbb')
    shutil.copy(paths.src_dir.onetbb / 'LICENSE.txt', paths.layer.onetbb / 'share/licenses/onetbb/LICENSE.txt')

  package(paths.layer.onetbb, paths.pkg.onetbb)

def openblas(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  with overlayfs_ro('/usr/local', [
    paths.toolchain.binutils / 'usr/local',
    paths.toolchain.crt / 'usr/local',
    paths.toolchain.gcc / 'usr/local',
    paths.toolchain.headers / 'usr/local',
  ]):
    triplet = MINGW_ARCH_2_TRIPLET_MAP[ver.arch]
    extra_flags = []

    if ver.arch == '32':
      extra_flags.extend([
        'TARGET=NORTHWOOD',
        'DYNAMIC_ARCH=1',
        'DYNAMIC_LIST=' + ' '.join([
          'NORTHWOOD', 'BANIAS',   # sse2
          'PRESCOTT',              # sse3
          'CORE2', 'ATOM',         # ssse3
          'PENRYN', 'DUNNINGTON',  # sse4.1
          'NEHALEM',               # sse4.2
          'OPTERON',               # sse2
          'OPTERON_SSE3',          # sse3
          'BARCELONA',             # sse4a
          'NANO',                  # ssse3
        ]),
      ])
    elif ver.arch == '64':
      if config.profile.startswith('64_v2-'):
        extra_flags.extend([
          'TARGET=NEHALEM',
          'DYNAMIC_ARCH=1',
          'DYNAMIC_LIST=' + ' '.join([
            'NEHALEM',                                              # sse4.2
            'SANDYBRIDGE',                                          # avx
            'HASWELL',                                              # avx2
            'SKYLAKEX', 'COOPERLAKE', 'SAPPHIRERAPIDS',             # avx512
            'BULLDOZER', 'PILEDRIVER', 'STEAMROLLER', 'EXCAVATOR',  # avx
            'ZEN',                                                  # avx2
          ]),
        ])
      else:
        extra_flags.extend([
          'TARGET=GENERIC',
          'DYNAMIC_ARCH=1',
          'DYNAMIC_LIST=' + ' '.join([
            'PRESCOTT',                                             # sse3
            'CORE2', 'ATOM',                                        # ssse3
            'PENRYN', 'DUNNINGTON',                                 # sse4.1
            'NEHALEM',                                              # sse4.2
            'SANDYBRIDGE',                                          # avx
            'HASWELL',                                              # avx2
            'SKYLAKEX', 'COOPERLAKE', 'SAPPHIRERAPIDS',             # avx512
            'OPTERON',                                              # sse2
            'OPTERON_SSE3',                                         # sse3
            'BARCELONA', 'BOBCAT',                                  # sse4a
            'BULLDOZER', 'PILEDRIVER', 'STEAMROLLER', 'EXCAVATOR',  # avx
            'ZEN',                                                  # avx2
            'NANO',                                                 # ssse3
          ]),
        ])
    else:
      raise Exception(f'Unsupported architecture: {ver.arch}')

    make_custom(paths.src_dir.openblas, [
      'NO_SHARED=1',
      'FIXED_LIBNAME=1',
      f'CC={triplet}-gcc',
      f'FC={triplet}-gfortran',
      f'AR={triplet}-gcc-ar',
      'HOSTCC=gcc',
      *extra_flags,
    ], config.jobs)
    make_custom(paths.src_dir.openblas, [
      'install',
      'PREFIX=/',
      f'DESTDIR={paths.layer.openblas}',
      'NO_SHARED=1',
      'FIXED_LIBNAME=1',
    ], jobs = 1)

    ensure(paths.layer.openblas / 'share/licenses/openblas')
    shutil.copy(paths.src_dir.openblas / 'LICENSE', paths.layer.openblas / 'share/licenses/openblas/LICENSE')

  package(paths.layer.openblas, paths.pkg.openblas)
