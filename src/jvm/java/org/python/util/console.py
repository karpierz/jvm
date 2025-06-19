# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

__all__ = ('prompt',)

import os

readline = None
try:
    import readline
except ImportError:
    try:
        import pyreadline as readline
    except ImportError:
        msg = """
              No readline available. History will not be available.
              """
        if os.name == "posix":
            msg += """
                   You may want to set the LD_PRELOAD environment variable.
                   See the README file for details.

                   i.e.: export LD_PRELOAD=/usr/lib/libpython2.7.so.1.0
                   """
        elif os.name == "nt":
            msg += """
                   For Windows use pyreadline and get it from the official git
                   repo on github:
                   https://github.com/pyreadline/pyreadline

                   Do NOT use the version on pypi.python.org, and therefore
                   Do NOT use the version installed by pip.  It is out of date
                   and doesn't work with Jep!
                   """
        print(msg)
except OSError as exc:
    if hasattr(exc, "winerror"):
        print(f"Windows error importing readline: {exc}")
        print("Please try using the latest pyreadline from "
              "https://github.com/pyreadline/pyreadline")
    else:
        print(f"Error importing readline: {exc}")

history_file = None
if readline is not None:
    try:
        import rlcompleter
        readline.set_completer(rlcompleter.Completer(locals()).complete)
        readline.parse_and_bind("tab: complete")
    except BaseException:
        pass
    try:
        history_file = os.path.join(os.path.expanduser("~"), ".jtypes")  # , ".jep")
        if not os.path.exists(history_file):
            open(history_file, "w").close()
            # readline.write_history_file(history_file)
        else:
            readline.read_history_file(history_file)
    except IOError:
        pass

del os


def prompt(python=None):

    # import code
    # con = code.InteractiveConsole([locals[, filename]])

    import sys
    # import traceback

    PS1 = getattr(sys, "ps1", ">>> ")
    PS2 = getattr(sys, "ps2", "... ")

    try:
        line = None
        ran  = True
        while True:
            try:
                line = input(PS1 if ran else PS2)
            except BaseException:
                break
            ran = True
            try:
                try:
                    ran = python.eval(line) if python else eval(line)
                except SyntaxError:
                    if python:
                        ran = python.execute(line)
                    else:
                        exec(line, None)
                        ran = True
            # except SystemExit:
            #     # if a user uses exit(), don't print the error
            #     pass
            except Exception as err:
                printed_err = False
                try:
                    if python and len(err.args) and "printStackTrace" in dir(err.args[0]):
                        err.args[0].printStackTrace()
                        printed_err = True
                except Exception as exc:
                    print(f"Error printing stacktrace: {exc}")
                finally:
                    if not printed_err:
                        print(f"{err}")
                # traceback.print_exc()
    finally:
        if history_file is not None:
            try:
                readline.write_history_file(history_file)
            except IOError:
                pass
