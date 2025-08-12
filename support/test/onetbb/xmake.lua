target("onetbb/pstl")
  add_files("pstl.cc")
  add_links("tbb")
  add_tests("default", { pass_output = "sorted\n" })
