#!/usr/bin/python3
from cnc.position import Position
from cnc.misc import Misc
from cnc.program import Program
from cnc.toollife import Tool


if __name__ == "__main__":

    # TODO：修改你的机床IP地址
    ip = '127.0.0.1'

    # 默认使用windows环境
    # TODO:修改环境，eg:position = Position(ip, win32=False)
    position = Position(ip)
    misc = Misc(ip)
    program = Program(ip)
    tool = Tool(ip)

    position()
    misc()
    program()
    position.close()
    # tool()
