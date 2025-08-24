target("fmt/fmt")
  on_config(pkgconf("fmt"))
  add_files("fmt.cc")
  add_tests("default", { pass_output = "Hello, World!" })

target("fmt/print")
  on_config(pkgconf("fmt"))
  add_files("print.cc")
  add_tests("default", { pass_output = "Hello, World!" })
