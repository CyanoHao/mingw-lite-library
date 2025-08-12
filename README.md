# MinGW Lite Library

Curated libraries built with MinGW Lite.

## Build

1. Prepare build environment. Linux:
   ```bash
   podman build -t mingw-lite/buildenv support/buildenv
   ```
   For Windows host, see [instructions from mingw-lite](https://github.com/redpanda-cpp/mingw-lite/blob/master/doc/wsl-buildenv.md).
2. Launch build environment. Linux:
   ```bash
   podman run -it --rm \
     --cap-add=sys_admin \
     -v $PWD:/mnt -w /mnt \
     mingw-lite/buildenv
   ```
   To expose build directories for debugging:
   ```bash
   podman run -it --rm \
     --cap-add=sys_admin \
     -v $PWD:/mnt -w /mnt \
     -v $PWD/build:/tmp/build \
     -v $PWD/layer:/tmp/layer \
     -v $PWD/pkg:/tmp/pkg \
     mingw-lite/buildenv
   ```
   Windows: in “Terminal”, select “mingw-lite-buildenv” from the dropdown list.
3. In the build environment, run:
   ```bash
   ./main.py -b <branch> -p <mingw-lite-profile> -mv <mingw-lite-version>
   ```

Available branches:

- [2026](./doc/2026.md)
- [2025](./doc/2025.md)
