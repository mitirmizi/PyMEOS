import platform
import sys

from cffi import FFI

ffibuilder = FFI()

with open("./pymeos_cffi/builder/meos.h", "r") as f:
    content = f.read()

ffibuilder.cdef(content)


def get_library_dirs():
    if sys.platform == "linux":
        return ["/usr/local/lib"]
    elif sys.platform == "darwin":
        if platform.processor() == "arm":
            return ["/opt/homebrew/lib"]
        else:
            return ["/usr/local/lib"]
    else:
        raise NotImplementedError("Unsupported platform")


ffibuilder.set_source(
    "_meos_cffi",
    '#include "meos.h"\n' '#include "meos_catalog.h"\n' '#include "meos_internal.h"',
    libraries=["meos"],
    library_dirs=get_library_dirs(),
)  # library name, for the linker

if __name__ == "__main__":  # not when running with setuptools
    ffibuilder.compile(verbose=True)
