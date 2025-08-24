add_rules("mode.debug", "mode.release")
set_policy("build.c++.modules.gcc.cxx11abi", true)
set_policy("network.mode", "private")

function pkgconf(name)
  return function (target)
    local cflags = os.iorunv("pkgconf", {"--static", "--cflags", name})
    for _, flag in ipairs(os.argv(cflags)) do
      if flag:startswith("-I") and #flag > 2 then
        local includedir = flag:sub(3)
        if includedir and os.isdir(includedir) then
          target:add("includedirs", includedir)
        end
      elseif flag:startswith("-D") and #flag > 2 then
        local define = flag:sub(3)
        target:add("defines", define)
      elseif flag:startswith("-") and #flag > 1 then
        target:add("cxflags", flag)
      end
    end
    local ldflags = os.iorunv("pkgconf", {"--static", "--libs", name})
    for _, flag in ipairs(os.argv(ldflags)) do
      if flag:startswith("-L") and #flag > 2 then
          local linkdir = flag:sub(3)
          if linkdir and os.isdir(linkdir) then
            target:add("linkdirs", linkdir)
          end
      elseif flag:startswith("-l") and #flag > 2 then
        local link = flag:sub(3)
        target:add("links", link)
      elseif flag:startswith("-") and #flag > 1 then
        target:add("ldflags", flag)
      end
    end
  end
end

includes("f/fmt/xmake.lua")
includes("o/onetbb/xmake.lua")
includes("o/openblas/xmake.lua")
