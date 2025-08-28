import argparse
import logging
from packaging.version import Version
from typing import Dict, Optional

from module.util import MINGW_ARCH_2_TRIPLET_MAP

class BranchVersions:
  version: str

  fmt: str                      # [EL] freeze minor

  onetbb: str                   # [EL] freeze minor
  openblas: str                 # [EL] freeze patch

  xmake: str = '3.0.1'

  def __init__(
      self,

      version: str,

      fmt: str,

      onetbb: str,
      openblas: str,
  ):
    self.version = version

    self.fmt = fmt

    self.onetbb = onetbb
    self.openblas = openblas

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

    onetbb = '2022.2.0',
    openblas='0.3.30',
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
