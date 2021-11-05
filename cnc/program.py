#!/usr/bin/python3
from .base import CNC
from .struct_ import *


class Program(CNC):
    def __init__(self, ip):
        super().__init__(ip)

    def cnc_rdproginfo(self):
        """
        读取实际轴进给率
        cnc_rdproginfo(unsigned short FlibHndl, short type, short length, ODBNC *prginfo)
        type=0:二进制放在结构体中；=1放在ASC中
        length=12或31
        :return:
        """
        odbnc = ODBNC()
        # 定义参数和返回值
        self.lib_so.cnc_rdproginfo.restype = c_short
        self.lib_so.cnc_rdproginfo.argtypes = (c_ushort, c_short, c_short, POINTER(ODBNC))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_rdproginfo(super().handle(), 0, 12, byref(odbnc))
            if ret:
                self.raise_error(ret)
        print("注册的程序数：", odbnc.u.bin.reg_prg)
        print("可用程序数：", odbnc.u.bin.unreg_prg)
        print("已用内存：", odbnc.u.bin.used_mem)
        print("可用内存：", odbnc.u.bin.unused_mem)

    def cnc_rdprgnum(self):
        """
        读取正在执行的程序号和主程序号
        :return:
        """
        odbpro = ODBPRO()
        # 定义参数和返回值
        self.lib_so.cnc_rdprgnum.restype = c_short
        self.lib_so.cnc_rdprgnum.argtypes = (c_ushort, POINTER(ODBPRO))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_rdprgnum(super().handle(), byref(odbpro))
            if ret:
                self.raise_error(ret)
        print("正在运行的程序号：", odbpro.data)
        print("主程序号：", odbpro.mdata)

    def cnc_exeprgname(self):
        """
        读取正在执行的程序的完整路径
        :return:
        """
        odbexeprg = ODBEXEPRG()
        # 定义参数和返回值
        self.lib_so.cnc_exeprgname.restype = c_short
        self.lib_so.cnc_exeprgname.argtypes = (c_ushort, POINTER(ODBEXEPRG))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_exeprgname(super().handle(), byref(odbexeprg))
            if ret:
                self.raise_error(ret)
        print("正在运行的程序的完整路径：", odbexeprg.name.decode())

    def __call__(self, *args, **kwargs):
        print("----------------程序信息----------------")
        self.cnc_rdprgnum()
        self.cnc_exeprgname()
        self.cnc_rdproginfo()


if __name__ == "__main__":
    prog = Program('127.0.0.1')
    prog()













