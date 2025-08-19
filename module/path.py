import argparse
from packaging.version import Version
from pathlib import Path
import tempfile
from typing import NamedTuple, Optional

from module.profile import BranchVersions

class SourcePaths(NamedTuple):
  fmt: Path

  jpeg_turbo: Path

  onetbb: Path
  openblas: Path
  opencv: Path
  opencv_ade: Path
  opencv_contrib: Path

  png: Path

  webp: Path

  zlib: Path

class LayerPaths(NamedTuple):
  prefix: Path

  fmt: Path

  jpeg_turbo: Path

  onetbb: Path
  openblas: Path
  opencv: Path

  png: Path

  webp: Path

  zlib: Path

class ToolchainPaths(NamedTuple):
  prefix: Path

  binutils: Path
  crt: Path
  gcc: Path
  headers: Path

class ProjectPaths:
  root_dir: Path
  abi_name: str

  assets_dir: Path
  dist_dir: Path
  patch_dir: Path

  library_pkg: Path
  mingw_pkg: Path
  cross_pkg: Path

  # build phase

  build_dir: Path
  layer_dir: Path
  pkg_dir: Path

  src_dir: SourcePaths
  src_arx: SourcePaths

  layer: LayerPaths
  pkg: LayerPaths

  toolchain: ToolchainPaths

  # test phase

  test_dir: Path
  test_src_dir: Path

  test_mingw_dir: Path
  test_xmake_dir: Path
  test_xmake_exe: Path
  test_xmake_pkg: Path

  def __init__(
    self,
    config: argparse.Namespace,
    ver: BranchVersions,
  ):
    self.root_dir = Path.cwd()
    mingw_branch = config.mingw_lite_version.split('-')[0].split('.')[0]
    abi_name = f'mingw{config.profile}-{mingw_branch}'

    self.assets_dir = self.root_dir / 'assets'
    self.dist_dir = self.root_dir / 'dist'
    self.patch_dir = self.root_dir / 'patch'

    self.library_pkg = self.dist_dir / f'lib{config.profile}-{mingw_branch}-{ver.version}.tar.zst'
    self.mingw_pkg = self.assets_dir / f'mingw{config.profile}-{config.mingw_lite_version}.tar.zst'
    self.cross_pkg = self.assets_dir / f'x-mingw{config.profile}-{config.mingw_lite_version}.tar.zst'

    # build phase

    self.build_dir = Path(f'/tmp/build/{config.branch}/{abi_name}')
    self.layer_dir = Path(f'/tmp/layer/{config.branch}/{abi_name}')
    self.pkg_dir = Path(f'{tempfile.gettempdir()}/pkg/{config.branch}/{abi_name}')

    src_name = SourcePaths(
      fmt = f'fmt-{ver.fmt}',

      jpeg_turbo = f'libjpeg-turbo-{ver.jpeg_turbo}',

      onetbb = f'oneTBB-{ver.onetbb}',
      openblas = f'OpenBLAS-{ver.openblas}',
      opencv = f'opencv-{ver.opencv}',
      opencv_ade = f'ade-{ver.opencv_ade}',
      opencv_contrib = f'opencv_contrib-{ver.opencv}',

      png = f'libpng-{ver.png}',

      webp = f'libwebp-{ver.webp}',

      zlib = f'zlib-{ver.zlib}',
    )

    self.src_dir = SourcePaths(
      fmt = self.build_dir / src_name.fmt,

      jpeg_turbo = self.build_dir / src_name.jpeg_turbo,

      onetbb = self.build_dir / src_name.onetbb,
      openblas = self.build_dir / src_name.openblas,
      opencv = self.build_dir / src_name.opencv,
      opencv_ade = self.build_dir / src_name.opencv_ade,
      opencv_contrib = self.build_dir / src_name.opencv_contrib,

      png = self.build_dir / src_name.png,

      webp = self.build_dir / src_name.webp,

      zlib = self.build_dir / src_name.zlib,
    )

    self.src_arx = SourcePaths(
      fmt = self.assets_dir / f'{src_name.fmt}.zip',

      jpeg_turbo = self.assets_dir / f'{src_name.jpeg_turbo}.tar.gz',

      onetbb = self.assets_dir / f'{src_name.onetbb}.tar.gz',
      openblas = self.assets_dir / f'{src_name.openblas}.tar.gz',
      opencv = self.assets_dir / f'{src_name.opencv}.tar.gz',
      opencv_ade = self.assets_dir / f'{src_name.opencv_ade}.tar.gz',
      opencv_contrib = self.assets_dir / f'{src_name.opencv_contrib}.tar.gz',

      png = self.assets_dir / f'{src_name.png}.tar.xz',

      webp = self.assets_dir / f'{src_name.webp}.tar.gz',

      zlib = self.assets_dir / f'{src_name.zlib}.tar.gz',
    )

    self.layer = LayerPaths(
      prefix = self.layer_dir,

      fmt = self.layer_dir / 'fmt',

      jpeg_turbo = self.layer_dir / 'jpeg-turbo',

      onetbb = self.layer_dir / 'onetbb',
      openblas = self.layer_dir / 'openblas',
      opencv = self.layer_dir / 'opencv',

      png = self.layer_dir / 'png',

      webp = self.layer_dir / 'webp',

      zlib = self.layer_dir / 'zlib',
    )

    self.pkg = LayerPaths(
      prefix = self.pkg_dir,

      fmt = self.pkg_dir / 'fmt.tar',

      jpeg_turbo = self.pkg_dir / 'jpeg-turbo.tar',

      onetbb = self.pkg_dir / 'onetbb.tar',
      openblas = self.pkg_dir / 'openblas.tar',
      opencv = self.pkg_dir / 'opencv.tar',

      png = self.pkg_dir / 'png.tar',

      webp = self.pkg_dir / 'webp.tar',

      zlib = self.pkg_dir / 'zlib.tar',
    )

    toolchain_dir = self.build_dir / abi_name
    self.toolchain = ToolchainPaths(
      prefix = toolchain_dir,

      binutils = toolchain_dir / 'AAB/binutils',
      crt = toolchain_dir / 'AAB/crt',
      gcc = toolchain_dir / 'AAB/gcc',
      headers = toolchain_dir / 'AAB/headers',
    )

    # test phase

    self.test_dir = Path(f'{tempfile.gettempdir()}/{config.branch}/{abi_name}')
    self.test_src_dir = self.root_dir / 'support' / 'test'

    self.test_mingw_dir = self.test_dir / abi_name
    self.test_xmake_dir = self.test_dir / 'xmake'
    self.test_xmake_exe = self.test_xmake_dir / 'xmake.exe'
    self.test_xmake_pkg = self.assets_dir / f'xmake-v{ver.xmake}.win64.zip'
