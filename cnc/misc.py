#!/usr/bin/python3
from .base import CNC
from .struct_ import *


class Misc(CNC):
    def __init__(self, ip):
        super().__init__(ip)

    def cnc_sysinfo_ex(self):
        """
        读取系统信息
        :return:
        """
        # 定义返回值和参数
        odbsysex = ODBSYSEX()
        self.lib_so.cnc_sysinfo_ex.restype = c_short
        self.lib_so.cnc_sysinfo_ex.argtypes = (c_ushort, POINTER(ODBSYSEX))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_sysinfo_ex(super().handle(), byref(odbsysex))
            if ret:
                CNC.raise_error(ret)
        print("有效轴数：", odbsysex.ctrl_axis)
        print("伺服数：", odbsysex.ctrl_srvo)

    def cnc_alarm2(self):
        """
        读取警告信息，适用于15i、30i、0i-D/F、PMi-A系列
        :return:
        """
        self.lib_so.cnc_alarm2.restype = c_short
        self.lib_so.cnc_alarm2.argtypes = (c_ushort, POINTER(c_long))
        self.connect()
        alarm = c_long(0)
        with CNC.lock:
            ret = self.lib_so.cnc_alarm2(super().handle(), byref(alarm))
            if ret:
                CNC.raise_error(ret)
        alarm = alarm.value

        # 获取警告的具体信息
        if alarm:
            index = 0
            i = 1
            while i < 2 ** 20:
                if alarm & i:
                    print("警告信息：", Alarm_info[index])
                i = i << 1
                index += 1

        else:
            print("警告信息：无")

    def cnc_gettimer(self):
        """
        读取系统时间信息
        :return:
        """
        # 定义返回值和参数
        iodbtimer_time = IODBTIMER()
        iodbtimer_time.type = 1
        iodbtimer_date = IODBTIMER()
        iodbtimer_date.type = 0
        self.lib_so.cnc_gettimer.restype = c_short
        self.lib_so.cnc_gettimer.argtypes = (c_ushort, POINTER(IODBTIMER))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_gettimer(super().handle(), byref(iodbtimer_time))
            if ret:
                CNC.raise_error(ret)
            ret = self.lib_so.cnc_gettimer(super().handle(), byref(iodbtimer_date))
            if ret:
                CNC.raise_error(ret)

        mydate = str(iodbtimer_date.data.date.month) + '.' + str(iodbtimer_date.data.date.date) \
                 + ',' + str(iodbtimer_date.data.date.year)
        mytime = str(iodbtimer_time.data.time.hour) + ':' + str(iodbtimer_time.data.time.minute) \
                 + ':' + str(iodbtimer_time.data.time.second)
        print(mytime, ' ', mydate)

    def cnc_statinfo(self):
        """
        读取CNC状态信息
        """
        odbst = ODBST()
        self.lib_so.cnc_statinfo.restype = c_short
        self.lib_so.cnc_statinfo.argtypes = (c_ushort, POINTER(ODBST))
        self.connect()
        with CNC.lock:
            ret = self.lib_so.cnc_statinfo(super().handle(), byref(odbst))
            if ret:
                CNC.raise_error(ret)
        print("自动模式状态：", AUT[odbst.aut])
        print("手动模式状态：", MANUAL[odbst.manual])
        print("运行信息：", RUN[odbst.run])
        print("轴运动状态：", MOTION[odbst.motion])
        print("紧急状态：", EMERGENCY[odbst.emergency])

    def __call__(self, *args, **kwargs):
        print("----------------警告信息----------------")
        self.cnc_alarm2()
        self.cnc_sysinfo_ex()
        print("----------------系统时间----------------")
        self.cnc_gettimer()
        print("----------------状态信息---------------")
        self.cnc_statinfo()


if __name__ == "__main__":
    misc = Misc('127.0.0.1')
    misc()
