target("fmt/fmt")
  on_config(pkgconf("fmt"))
  add_files("fmt.cc")
  add_tests("default", { pass_outputs = "Hello, world!\n" })

target("fmt/print")
  on_config(pkgconf("fmt"))
  add_files("print.cc")
  add_tests("default", { pass_outputs = "Hello, world!\n" })
