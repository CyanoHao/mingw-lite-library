import argparse
import os
import shutil
import subprocess

from module.debug import shell_here
from module.path import ProjectPaths
from module.profile import BranchProfile
from module.util import MINGW_ARCH_2_TRIPLET_MAP
from module.util import ensure, overlayfs_ro, package
from module.util import cflags, configure, make_default, make_destdir_install

def zlib(ver: BranchProfile, paths: ProjectPaths, config: argparse.Namespace):
  build_dir = paths.src_dir.zlib / 'build'
  ensure(build_dir)

  with overlayfs_ro('/usr/local', [
    paths.toolchain.binutils / 'usr/local',
    paths.toolchain.crt / 'usr/local',
    paths.toolchain.gcc / 'usr/local',
    paths.toolchain.headers / 'usr/local',
  ]):
    subprocess.run([
      '../configure',
      '--prefix=',
      '--static',
    ], cwd = build_dir, check = True, env = {
      **os.environ,
      'CHOST': MINGW_ARCH_2_TRIPLET_MAP[ver.arch],
    })
    make_default(build_dir, config.jobs)
    make_destdir_install(build_dir, paths.layer.zlib)

    ensure(paths.layer.zlib / 'share/licenses/zlib')
    shutil.copy(paths.src_dir.zlib / 'LICENSE', paths.layer.zlib / 'share/licenses/zlib/LICENSE')

  package(paths.layer.zlib, paths.pkg.zlib)
