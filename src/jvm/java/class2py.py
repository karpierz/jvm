# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.


def class2py(class_file, header=None):
    from pathlib import Path
    from codecs import encode
    import io
    import re
    py_file    = Path(class_file.replace("$", "_")).with_suffix(".py")
    class_file = Path(class_file)
    is_new_py  = not py_file.exists()
    jcode_rexp = re.compile(r"(?P<beg>(.*\n)*)[ \t]*__javacode__[ \t]*="
                            r"\s*(((.|\n)*?\((.|\n)*?\))|(None[ \t]*\n))"
                            r"(?P<end>(.|\n)*)")
    if header is None:
        header = """\
# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

"""
    footer = """
"""
    with class_file.open("rb") as fi, \
         py_file.open("a+t", newline="") as fo, \
         io.StringIO() as tmp:
        fo.seek(0)
        content = fo.read()
        match = jcode_rexp.match(content)
        beg = match.group("beg") if match else ""
        end = match.group("end") if match else ""
        print(header if is_new_py else beg, end="", file=tmp)
        if is_new_py: print("__jnimethods__ = (\n)\n", file=tmp)
        print("__javacode__ = bytearray(  # Auto-generated; DO NOT EDIT!", file=tmp)
        while True:
            row = fi.read(20)
            if not row:
                break
            line = "".join(r"\x%c%c" % (c1, c2)
                           for c1, c2 in zip(*[iter(encode(row, "hex"))] * 2))
            print('    b"{}"'.format(line), file=tmp)
        print(")", end="", file=tmp)
        print(footer if is_new_py else end, end="", file=tmp)
        if tmp.getvalue() != content:
            fo.seek(0)
            fo.truncate()
            fo.write(tmp.getvalue())


if __name__ == "__main__":
    import sys
    class2py(sys.argv[1])
