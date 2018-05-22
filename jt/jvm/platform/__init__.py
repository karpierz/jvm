# Copyright (c) 2004-2018 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from ..lib import platform

if platform.is_cygwin:
    from ._cygwin  import JVMFinder
elif platform.is_windows:
    from ._windows import JVMFinder
elif platform.is_linux:
    from ._linux   import JVMFinder
elif platform.is_osx:
    from ._osx     import JVMFinder
elif platform.is_android:
    from ._android import JVMFinder
elif platform.is_posix:
    from ._linux   import JVMFinder
else:
    raise ImportError("unsupported platform")

del platform
