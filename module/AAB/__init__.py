import argparse

from module.path import ProjectPaths
from module.profile import BranchVersions

import module.AAB.o as o

def build_AAB_library(ver: BranchVersions, paths: ProjectPaths, config: argparse.Namespace):
  o.onetbb(ver, paths, config)
  o.openblas(ver, paths, config)
