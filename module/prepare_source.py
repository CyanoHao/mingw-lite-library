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

from module.fetch import validate_and_download, check_and_extract, patch, patch_done
from module.path import ProjectPaths
from module.profile import BranchProfile

def _fmt(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/fmtlib/fmt/releases/download/{ver.fmt}/{paths.src_arx.fmt.name}'
  validate_and_download(paths.src_arx.fmt, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.fmt, paths.src_arx.fmt)
  patch_done(paths.src_dir.fmt)

def _jpeg_turbo(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/libjpeg-turbo/libjpeg-turbo/releases/download/{ver.jpeg_turbo}/{paths.src_arx.jpeg_turbo.name}'
  validate_and_download(paths.src_arx.jpeg_turbo, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.jpeg_turbo, paths.src_arx.jpeg_turbo)
  patch_done(paths.src_dir.jpeg_turbo)

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

  if check_and_extract(paths.src_dir.openblas, paths.src_arx.openblas):
    # Fix pkgconfig relocation
    patch(paths.src_dir.openblas, paths.patch_dir / 'openblas/fix-pkgconfig-relocation.patch')

    patch_done(paths.src_dir.openblas)

def _opencv(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/opencv/opencv/archive/refs/tags/{ver.opencv}.tar.gz'
  validate_and_download(paths.src_arx.opencv, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.opencv, paths.src_arx.opencv)
  patch_done(paths.src_dir.opencv)

def _opencv_ade(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/opencv/ade/archive/refs/tags/v{ver.opencv_ade}.tar.gz'
  validate_and_download(paths.src_arx.opencv_ade, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.opencv_ade, paths.src_arx.opencv_ade)
  patch_done(paths.src_dir.opencv_ade)

def _opencv_contrib(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://github.com/opencv/opencv_contrib/archive/refs/tags/{ver.opencv}.tar.gz'
  validate_and_download(paths.src_arx.opencv_contrib, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.opencv_contrib, paths.src_arx.opencv_contrib)
  patch_done(paths.src_dir.opencv_contrib)

def _png(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  v = Version(ver.png)
  abi = f'{v.major}{v.minor}'
  url = f'https://downloads.sourceforge.net/project/libpng/libpng{abi}/{ver.png}/{paths.src_arx.png.name}'
  validate_and_download(paths.src_arx.png, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.png, paths.src_arx.png)
  patch_done(paths.src_dir.png)

def _webp(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://storage.googleapis.com/downloads.webmproject.org/releases/webp/{paths.src_arx.webp.name}'
  validate_and_download(paths.src_arx.webp, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.webp, paths.src_arx.webp)
  patch_done(paths.src_dir.webp)

def _zlib(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  url = f'https://zlib.net/fossils/{paths.src_arx.zlib.name}'
  validate_and_download(paths.src_arx.zlib, url)
  if download_only:
    return

  check_and_extract(paths.src_dir.zlib, paths.src_arx.zlib)
  patch_done(paths.src_dir.zlib)

def prepare_source(ver: BranchProfile, paths: ProjectPaths, download_only: bool):
  _fmt(ver, paths, download_only)

  _jpeg_turbo(ver, paths, download_only)

  _onetbb(ver, paths, download_only)
  _openblas(ver, paths, download_only)
  _opencv(ver, paths, download_only)
  _opencv_ade(ver, paths, download_only)
  _opencv_contrib(ver, paths, download_only)

  _png(ver, paths, download_only)

  _webp(ver, paths, download_only)

  _zlib(ver, paths, download_only)
