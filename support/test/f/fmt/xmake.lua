target("fmt/fmt")
  add_files("fmt.cc")
  add_links("fmt")
  add_tests("default", { pass_outputs = "Hello, world!\n" })

target("fmt/print")
  add_files("print.cc")
  add_links("fmt")
  add_tests("default", { pass_outputs = "Hello, world!\n" })
