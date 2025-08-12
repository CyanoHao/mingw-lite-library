from hashlib import sha256
import logging
import os
from packaging.version import Version
from pathlib import Path
import re
import shutil
import subprocess
from urllib.error import URLError
from urllib.request import urlopen

from module.fetch import validate_and_download, check_and_extract, patch_done
from module.path import ProjectPaths
from module.profile import BranchProfile

def _patch(path: Path, patch: Path):
  res = subprocess.run([
    'patch',
    '-Np1',
    '-i', patch,
  ], cwd = path)
  if res.returncode != 0:
    message = 'Patch fail: applying %s to %s' % (patch.name, path.name)
    logging.critical(message)
    raise Exception(message)

def _onetbb(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/uxlfoundation/oneTBB/archive/refs/tags/v{ver.onetbb}.tar.gz'
  validate_and_download(paths.src_arx.onetbb, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.onetbb, paths.src_arx.onetbb)
  patch_done(paths.src_dir.onetbb)

def _openblas(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/OpenMathLib/OpenBLAS/releases/download/v{ver.openblas}/{paths.src_arx.openblas.name}'
  validate_and_download(paths.src_arx.openblas, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.openblas, paths.src_arx.openblas)
  patch_done(paths.src_dir.openblas)

def prepare_source(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  _onetbb(ver, paths, download_only)
  _openblas(ver, paths, download_only)
