import argparse

from module.path import ProjectPaths
from module.profile import BranchVersions

import module.AAB.f as f
import module.AAB.j as j
import module.AAB.o as o
import module.AAB.p as p
import module.AAB.w as w
import module.AAB.z as z

def build_AAB_library(ver: BranchVersions, paths: ProjectPaths, config: argparse.Namespace):
  ###########
  # Round 1 #
  ###########

  f.fmt(ver, paths, config)

  j.jpeg_turbo(ver, paths, config)

  o.onetbb(ver, paths, config)
  o.openblas(ver, paths, config)

  w.webp(ver, paths, config)

  z.zlib(ver, paths, config)

  ###########
  # Round 2 #
  ###########

  p.png(ver, paths, config)  # dep: zlib

  ###########
  # Round 3 #
  ###########

  o.opencv(ver, paths, config)  # dep: jpeg_turbo, png, webp, zlib
