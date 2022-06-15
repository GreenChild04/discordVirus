from pathlib import Path
from sys import *
import os
import base64


def openFile(file):
    with Path(file) as file:
        contents = file.read_text()
        return contents


def to64(contents):
    byte = contents.encode("ascii")
    b64 = base64.b85encode(byte)
    return b64.decode("ascii")


def from64(contents):
    normal = base64.b85decode(contents)
    return normal.decode()


def writeTheThing(data, loc):
    with Path(loc) as file:
        file.write_text(data)


if __name__ == '__main__':
    if argv[1] == "-t":
        a = openFile(argv[2])
        b = to64(a)
        print(b)
        writeTheThing(b, argv[2].split(".")[0])
    elif argv[1] == "-f":
        a = openFile(argv[2])
        c = from64(a)
        print(c)
        writeTheThing(c, argv[2] + ".py")
