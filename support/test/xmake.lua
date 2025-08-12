add_rules("mode.debug", "mode.release")
set_policy("build.c++.modules.gcc.cxx11abi", true)

includes("onetbb/xmake.lua")
includes("openblas/xmake.lua")
