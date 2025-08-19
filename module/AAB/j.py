import argparse
import os
import shutil

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchProfile
from module.util import ensure, overlayfs_ro, package
from module.util import configure, make_default, make_destdir_install
from module.util import cmake_build, cmake_config, cmake_flags, cmake_install

def jpeg_turbo(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  license_dir = paths.layer.jpeg_turbo / 'share/licenses/jpeg-turbo'
  ensure(license_dir)

  with overlayfs_ro('/usr/local', [
    paths.toolchain.binutils / 'usr/local',
    paths.toolchain.crt / 'usr/local',
    paths.toolchain.gcc / 'usr/local',
    paths.toolchain.headers / 'usr/local',
  ]):
    cmake_config(paths.src_dir.jpeg_turbo, [
      '-DCMAKE_INSTALL_PREFIX=/usr/local',
      '-DENABLE_SHARED=OFF',
      '-DENABLE_STATIC=ON',
      *cmake_flags(ver.arch, ver.optimize_for_size),
    ])
    cmake_build(paths.src_dir.jpeg_turbo, config.jobs)
    cmake_install(paths.src_dir.jpeg_turbo, paths.layer.jpeg_turbo)

    shutil.rmtree(paths.layer.jpeg_turbo / 'bin')

    shutil.copy(paths.src_dir.jpeg_turbo / 'LICENSE.md', license_dir / 'LICENSE.md')

  package(paths.layer.jpeg_turbo, paths.pkg.jpeg_turbo)
