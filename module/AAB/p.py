import argparse
import os
from packaging.version import Version
import shutil

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchProfile
from module.util import ensure, overlayfs_ro, package
from module.util import configure, make_default, make_destdir_install
from module.util import cmake_build, cmake_config, cmake_flags, cmake_install

def png(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  license_dir = paths.layer.png / 'share/licenses/png'
  ensure(license_dir)

  v = Version(ver.png)
  png_abi = f'{v.major}{v.minor}'

  with overlayfs_ro('/usr/local', [
    paths.toolchain.binutils / 'usr/local',
    paths.toolchain.crt / 'usr/local',
    paths.toolchain.gcc / 'usr/local',
    paths.toolchain.headers / 'usr/local',

    paths.layer.zlib,
  ]):
    cmake_config(paths.src_dir.png, [
      '-DPNG_SHARED=OFF',
      '-DPNG_STATIC=ON',
      '-DPNG_TESTS=OFF',
      '-DPNG_TOOLS=OFF',
      *cmake_flags(ver.arch, ver.optimize_for_size),
    ])
    cmake_build(paths.src_dir.png, config.jobs)
    cmake_install(paths.src_dir.png, paths.layer.png)

    shutil.rmtree(paths.layer.png / 'bin')

    shutil.copy(paths.src_dir.png / 'LICENSE', license_dir / 'LICENSE')

    # replace soft links with hard links
    os.remove(paths.layer.png / 'lib/libpng.a')
    os.link(
      paths.layer.png / f'lib/libpng{png_abi}.a',
      paths.layer.png / 'lib/libpng.a',
    )
    os.remove(paths.layer.png / 'lib/pkgconfig/libpng.pc')
    os.link(
      paths.layer.png / f'lib/pkgconfig/libpng{png_abi}.pc',
      paths.layer.png / 'lib/pkgconfig/libpng.pc'
    )

  package(paths.layer.png, paths.pkg.png)
  with open(paths.pkg_dir / 'png.dep.txt', 'w') as f:
    f.write('zlib\n')
