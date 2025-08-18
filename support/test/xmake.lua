add_rules("mode.debug", "mode.release")
set_policy("build.c++.modules.gcc.cxx11abi", true)

includes("f/fmt/xmake.lua")
includes("o/onetbb/xmake.lua")
includes("o/openblas/xmake.lua")
