import argparse
import os
import shutil

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchProfile
from module.util import cmake_build, cmake_config, cmake_flags, cmake_install, ensure, make_custom, overlayfs_ro, package, MINGW_ARCH_2_TRIPLET_MAP

def fmt(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  with overlayfs_ro('/usr/local', [
    paths.toolchain.binutils / 'usr/local',
    paths.toolchain.crt / 'usr/local',
    paths.toolchain.gcc / 'usr/local',
    paths.toolchain.headers / 'usr/local',
  ]):
    cmake_config(paths.src_dir.fmt, [
      '-DBUILD_SHARED_LIBS=OFF',
      '-DFMT_TEST=OFF',
      *cmake_flags(ver.arch, ver.optimize_for_size),
    ])
    cmake_build(paths.src_dir.fmt, config.jobs)
    cmake_install(paths.src_dir.fmt, paths.layer.fmt)

    ensure(paths.layer.fmt / 'share/licenses/fmt')
    shutil.copy(paths.src_dir.fmt / 'LICENSE', paths.layer.fmt / 'share/licenses/fmt/LICENSE')

  package(paths.layer.fmt, paths.pkg.fmt)
