add_requires("pkgconfig::fmt", {alias = "fmt", system = true})

target("fmt/fmt")
  add_packages("fmt")
  add_files("fmt.cc")
  add_tests("default", { pass_output = "Hello, World!" })

target("fmt/print")
  add_packages("fmt")
  add_files("print.cc")
  add_tests("default", { pass_output = "Hello, World!" })
