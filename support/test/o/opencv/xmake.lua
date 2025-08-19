target("opencv/imread")
  on_config(pkgconf("opencv4"))
  add_files("imread.cc")
  set_rundir(".")
  add_tests("default", {
    pass_outputs =
      "Image size: [8 x 8]\n" ..
      "Black pixel ok: 1\n" ..
      "White pixel ok: 1\n" ..
      "Image size: [8 x 8]\n" ..
      "Black pixel ok: 1\n" ..
      "White pixel ok: 1\n" ..
      "Image size: [8 x 8]\n" ..
      "Black pixel ok: 1\n" ..
      "White pixel ok: 1\n",
    plain = true})
