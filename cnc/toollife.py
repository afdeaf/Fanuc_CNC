#!/usr/bin/python3
from .base import CNC
from .struct_ import *


class Tool(CNC):
    def __init__(self, ip):
        super().__init__(ip)

    def cnc_rdgrpid2(self, number=0):
        """
        根据给定的刀具号，读取其组号
        :return:
        """
        pass

    def cnc_rdngrp(self):
        """
        读取刀具一共有多少组
        :return:
        """
        odbtlife2 = ODBTLIFE2()
        self.lib_so.cnc_rdngrp.restype = c_short
        self.lib_so.cnc_rdngrp.argtypes = (c_ushort, POINTER(ODBTLIFE2))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_rdngrp(super().handle(), byref(odbtlife2))
            if ret:
                CNC.raise_error(ret)
        print("刀具组数：", odbtlife2.data)
        return odbtlife2.data

    def cnc_rdlife(self, number=1):
        """
        读取给定组号的刀具的寿命
        :param number:组号
        :return:
        """
        odbtlife3 = ODBTLIFE3()
        self.lib_so.cnc_rdlife.restype = c_short
        self.lib_so.cnc_rdlife.argtypes = (c_ushort, c_short, POINTER(ODBTLIFE3))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_rdlife(super().handle(), number, byref(odbtlife3))
            if ret:
                CNC.raise_error(ret)
        print("刀具组{}的寿命：{}".format(number, odbtlife3.data))

    def cnc_rdusetlno(self, s_grp=1, e_grp=2, length=12):
        """
        读取指定组的刀具执行号？
        :return:
        """
        odbtluse = ODBTLUSE()
        self.lib_so.cnc_rdusetlno.restype = c_short
        self.lib_so.cnc_rdusetlno.argtypes = (c_ushort, c_short, c_short, c_short, POINTER(ODBTLUSE))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_rdusetlno(super().handle(), s_grp, e_grp, length, byref(odbtluse))
            if ret:
                CNC.raise_error(ret)
        print("刀具执行号：", odbtluse.data)

    def cnc_rdtlusegrp(self):
        """
        读取已经使用的组号
        :return:
        """
        odbusergrp = ODBUSEGRP()
        self.lib_so.cnc_rdtlusegrp.restype = c_short
        self.lib_so.cnc_rdtlusegrp.argtypes = (c_ushort, POINTER(ODBUSEGRP))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_rdtlusegrp(super().handle(), byref(odbusergrp))
            if ret:
                CNC.raise_error(ret)
        print("当前刀具组号：", odbusergrp.use)
        return odbusergrp.use

    def __call__(self, *args, **kwargs):
        print("----------------刀具寿命信息----------------")
        self.cnc_rdngrp()
        use = self.cnc_rdtlusegrp()
        self.cnc_rdlife(use)
        self.cnc_rdusetlno()


if __name__ == "__main__":
    tool = Tool('127.0.0.1')
    tool()
