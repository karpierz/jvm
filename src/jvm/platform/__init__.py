# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from ..lib import platform

if platform.is_cygwin:
    from ._cygwin  import *  # noqa
elif platform.is_windows:
    from ._windows import *  # noqa
elif platform.is_linux:
    from ._linux   import *  # noqa
elif platform.is_macos:
    from ._macos   import *  # noqa
elif platform.is_android:
    from ._android import *  # noqa
elif platform.is_posix:
    from ._linux   import *  # noqa
else:
    raise ImportError("unsupported platform")

del platform
