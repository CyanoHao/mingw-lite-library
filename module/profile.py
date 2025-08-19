import argparse
import logging
from packaging.version import Version
from typing import Dict, Optional

from module.util import MINGW_ARCH_2_TRIPLET_MAP

class BranchVersions:
  version: str

  fmt: str                      # freeze minor

  jpeg_turbo: str               # freeze minor

  onetbb: str                   # freeze minor
  openblas: str                 # freeze patch
  opencv: str                   # freeze minor
  opencv_ade: str               # freeze patch

  png: str                      # freeze patch

  webp: str                     # freeze minor

  zlib: str                     # freeze minor

  xmake: str = '3.0.1'

  def __init__(
      self,

      version: str,

      fmt: str,

      jpeg_turbo: str,

      onetbb: str,
      openblas: str,
      opencv: str,
      opencv_ade: str,

      png: str,

      webp: str,

      zlib: str,
  ):
    self.version = version

    self.fmt = fmt

    self.jpeg_turbo = jpeg_turbo

    self.onetbb = onetbb
    self.openblas = openblas
    self.opencv = opencv
    self.opencv_ade = opencv_ade

    self.png = png

    self.webp = webp

    self.zlib = zlib

class BranchProfile(BranchVersions):
  arch: str
  optimize_for_size: bool
  lto: bool

  def __init__(
    self,
    ver: BranchVersions,
    arch: str,
    optimize_for_size: bool,
  ):
    BranchVersions.__init__(self, **ver.__dict__)

    self.arch = arch
    self.optimize_for_size = optimize_for_size
    self.lto = not optimize_for_size

BRANCHES: Dict[str, BranchVersions] = {
  '2026': BranchVersions(
    version = '2026.0.0',

    fmt = '11.2.0',

    jpeg_turbo = '3.1.1',

    onetbb = '2022.2.0',
    openblas='0.3.30',
    opencv = '4.12.0',
    opencv_ade = '0.1.2e',

    png = '1.6.50',

    webp = '1.6.0',

    zlib = '1.3.1',
  ),
}

def resolve_profile(config: argparse.Namespace) -> BranchProfile:
  mingw_lite_arch_variant = config.profile.split('-')[0]
  mingw_arch = mingw_lite_arch_variant.split('_')[0]
  if mingw_arch not in MINGW_ARCH_2_TRIPLET_MAP:
    message = f'Invalid mingw profile: {config.profile} (arch = {mingw_arch})'
    logging.error(message)
    raise ValueError(message)

  if mingw_lite_arch_variant in ['64_v2', 'arm64']:
    optimize_for_size = False
  else:
    optimize_for_size = True

  return BranchProfile(
    ver = BRANCHES[config.branch],
    arch = mingw_arch,
    optimize_for_size = optimize_for_size,
  )
