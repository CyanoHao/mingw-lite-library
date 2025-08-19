import argparse
import os
import shutil

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchProfile
from module.util import ensure, overlayfs_ro, package
from module.util import configure, make_default, make_destdir_install
from module.util import cmake_build, cmake_config, cmake_flags, cmake_install

def webp(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  license_dir = paths.layer.webp / 'share/licenses/webp'
  ensure(license_dir)

  with overlayfs_ro('/usr/local', [
    paths.toolchain.binutils / 'usr/local',
    paths.toolchain.crt / 'usr/local',
    paths.toolchain.gcc / 'usr/local',
    paths.toolchain.headers / 'usr/local',
  ]):
    cmake_config(paths.src_dir.webp, [
      '-DBUILD_SHARED_LIBS=OFF',
      '-DWEBP_BUILD_ANIM_UTILS=OFF',
      '-DWEBP_BUILD_CWEBP=OFF',
      '-DWEBP_BUILD_DWEBP=OFF',
      '-DWEBP_BUILD_GIF2WEBP=OFF',
      '-DWEBP_BUILD_IMG2WEBP=OFF',
      '-DWEBP_BUILD_VWEBP=OFF',
      '-DWEBP_BUILD_WEBPINFO=OFF',
      '-DWEBP_BUILD_WEBPMUX=OFF',
      *cmake_flags(ver.arch, ver.optimize_for_size),
    ])
    cmake_build(paths.src_dir.webp, config.jobs)
    cmake_install(paths.src_dir.webp, paths.layer.webp)

    shutil.copy(paths.src_dir.webp / 'COPYING', license_dir / 'COPYING')

  package(paths.layer.webp, paths.pkg.webp)
