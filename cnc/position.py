#!/usr/bin/python3
from .base import CNC
from .struct_ import *


class Position(CNC):
    def __init__(self, ip):
        super().__init__(ip)

    def cnc_actf(self):
        """
        读取实际轴进给率
        :return:
        """
        odbact = ODBACT()
        # 定义参数和返回值
        self.lib_so.cnc_actf.restype = c_short
        self.lib_so.cnc_actf.argtypes = (c_ushort, POINTER(ODBACT))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_actf(super().handle(), byref(odbact))

            if ret:
                self.raise_error(ret)
        print("进给率：", odbact.data)

    def cnc_absolute2(self, axis=-1):
        """
        读取绝对轴位置，读取的是CNC屏幕上显示的数据
        :return:
        """
        # 定义返回值和参数
        odbaxis = ODBAXIS()
        self.lib_so.cnc_absolute2.restype = c_short
        self.lib_so.cnc_absolute2.argtypes = (c_ushort, c_short, c_short, POINTER(ODBAXIS))
        length = 4 + 4 * MAX_AXIS  # ODBAXIS结构体的size
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_absolute2(super().handle(), axis, length, byref(odbaxis))
            if ret:
                self.raise_error(ret)
        x, y, z = str(odbaxis.data[0]), str(odbaxis.data[1]), str(odbaxis.data[2])
        if len(x) < 3:
            pass
        print("轴绝对位置(x, y, z)：", (odbaxis.data[0]/1000, odbaxis.data[1]/1000, odbaxis.data[2]/1000))

    def cnc_machine(self, axis=1):
        """
        读取机器指定轴位置
        :return:
        """
        odbaxis = ODBAXIS()
        self.lib_so.cnc_machine.restype = c_short
        self.lib_so.cnc_machine.argtypes = (c_ushort, c_short, c_short, POINTER(ODBAXIS))
        length = 8  # ODBAXIS结构体的size
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_machine(super().handle(), axis, length, byref(odbaxis))
            if ret:
                self.raise_error(ret)

        # 数据存储在data[0]
        print("机器轴位置：", odbaxis.data[0])

    def cnc_relative2(self, axis=-1):
        """
        读取轴的相对位置，读取的是显示在CNC屏幕上数据
        :return:
        """
        odbaxis = ODBAXIS()
        self.lib_so.cnc_relative2.restype = c_short
        self.lib_so.cnc_relative2.argtypes = (c_ushort, c_short, c_short, POINTER(ODBAXIS))
        length = 4 + 4 * MAX_AXIS  # ODBAXIS结构体的size
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_relative2(super().handle(), axis, length, byref(odbaxis))
            if ret:
                self.raise_error(ret)
        print("轴相对位置(x, y, z)：", (odbaxis.data[0]/1000, odbaxis.data[1]/1000, odbaxis.data[2]/1000))

    def cnc_distance(self, axis=1):
        """
        读取轴还要移动的距离
        :return:
        """
        odbaxis = ODBAXIS()
        self.lib_so.cnc_distance.restype = c_short
        self.lib_so.cnc_distance.argtypes = (c_ushort, c_short, c_short, POINTER(ODBAXIS))
        length = 8  # ODBAXIS结构体的size
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_distance(super().handle(), axis, length, byref(odbaxis))
            if ret:
                self.raise_error(ret)
        print("轴还要移动的距离：", odbaxis.data[0])

    def cnc_srvdelay(self, axis=1):
        """
        读取给定轴的伺服延迟
        :return:
        """
        odbaxis = ODBAXIS()
        self.lib_so.cnc_srvdelay.restype = c_short
        self.lib_so.cnc_srvdelay.argtypes = (c_ushort, c_short, c_short, POINTER(ODBAXIS))
        length = 8  # ODBAXIS结构体的size
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_srvdelay(super().handle(), axis, length, byref(odbaxis))
            if ret:
                self.raise_error(ret)
        print("私服延迟：", odbaxis.data[0])

    def cnc_accdecdly(self, axis=1):
        """
        读取给定轴的加速/减速延迟
        :return:
        """
        odbaxis = ODBAXIS()
        self.lib_so.cnc_accdecdly.restype = c_short
        self.lib_so.cnc_accdecdly.argtypes = (c_ushort, c_short, c_short, POINTER(ODBAXIS))
        length = 8  # ODBAXIS结构体的size
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_accdecdly(super().handle(), axis, length, byref(odbaxis))
            if ret:
                self.raise_error(ret)
        print("加速/减速延迟：", odbaxis.data[0])

    def cnc_acts2(self, sp_no=1):
        """
        读取给定主轴实际转速，cnc_acts只能读取主轴的设置参数
        0i-F的sp_no最大值是8
        :return:
        """
        odbact2 = ODBACT2()
        self.lib_so.cnc_acts2.restype = c_short
        self.lib_so.cnc_acts2.argtypes = (c_ushort, c_short, POINTER(ODBACT2))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_acts2(super().handle(), sp_no, byref(odbact2))
            if ret:
                self.raise_error(ret)
        print("主轴转速：", odbact2.data[0], 'rpm')

    def cnc_rdspcss(self):
        """
        读取与CNC表面速度控制相关的数据。表面速度是指刀具最外点的线速度。
        此函数要求CNC支持表面速度控制。
        :return:
        """
        odbcss = ODBCSS()
        self.lib_so.cnc_rdspcss.restype = c_short
        self.lib_so.cnc_rdspcss.argtypes = (c_ushort, POINTER(ODBCSS))
        self.connect()
        with super().lock:
            ret = self.lib_so.cnc_rdspcss(super().handle(), byref(odbcss))
            if ret:
                self.raise_error(ret)

        print("转换过的主轴转速：", odbcss.srpm)
        print("表面速度：", odbcss.sspm)
        print("最大转速时的钳位电压：", odbcss.smax)

    def cnc_rdspeed(self):
        """
        读取主轴的实际转速和进给率
        :return:
        """
        odbspeed = ODBSPEED()
        self.lib_so.cnc_rdspeed.restype = c_short
        self.lib_so.cnc_rdspeed.argtypes = (c_ushort, POINTER(ODBSPEED))
        self.connect()
        with super().lock:
            ret = self.lib_so.cnc_rdspeed(super().handle(), byref(odbspeed))
            if ret:
                self.raise_error(ret)

        print("主轴进给率：", odbspeed.actf.data)
        print("主轴速度：", odbspeed.acts.data)

    def int2float(self, data):
        pass

    def __call__(self, *args, **kwargs):
        print("----------------位置信息----------------")
        self.cnc_actf()
        self.cnc_absolute2()
        self.cnc_machine()
        self.cnc_relative2()
        self.cnc_distance()
        self.cnc_srvdelay()
        self.cnc_accdecdly()
        # self.cnc_acts2()
        self.cnc_rdspcss()
        # self.cnc_rdspeed()


if __name__ == "__main__":
    pos = Position('127.0.0.1')
    pos()
