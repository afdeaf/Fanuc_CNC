#!/usr/bin/python3
from ctypes import *
from threading import RLock


class CNC(object):
    lock = RLock()   # 互斥锁
    __is_open = False
    __handle = c_ushort(0)

    @classmethod
    def raise_error(cls, error_code):
        cnc_error_dic = {
            -17: '[EW_PROTOCOL] 协议错误，从网卡返回的数据错误。',
            -16: '[EW_SOCKET] 网络连接失败。',
            -15: '[EW_NODLL] 指定的节点没有对应的CNC dll。',
            -11: '[EW_BUS] CNC总线错误，请联系供应商。',
            -10: '[EW_SYSTEM2] CNC系统错误。',
            -9: '[EW_HSSB] HSSB错误，请检查HSSB主板',
            -8: '[EW_HANDLE] 句柄号错误。',
            -7: '[EW_VERSION] CNC/PMC库版本号错误。',
            -6: '[EW_UNEXP] 库状态异常。',
            -5: '[EW_SYSTEM] 系统错误(使用HSSB通信时)。',
            -4: '[EW_PARITY] 共享内存错误(使用HSSB通信时)。',
            -3: '[EW_MMCSYS] FANUC驱动安装错误(使用HSSB通信时)。',
            -2: '[EW_RESET] 重置或中断请求。',
            -1: '[EW_BUSY] CNC忙，请等待当前处理完成。',
            1: '[EW_FUNC] 函数未执行，或不可用。',
            2: '[EW_LENGTH] 数据块长度错误、数据个数错误。',
            3: '[EW_NUMBER] 数据个数错误。',
            4: '[EW_ATTRIB] 数据属性错误。',
            5: '[EW_DATA] 找不到指定程序。',
            6: '[EW_NOOPT] CNC不支持该操作。',
            7: '[EW_PROT] 禁止执行写操作。',
            8: '[EW_OVRFLOW] CNC内存溢出。',
            9: '[EW_PARAM] CNC参数设置错误。',
            10: '[EW_BUFFER] 缓冲区空/满，请等待CNC执行完成。',
            11: '[EW_PATH] 路径号错误。',
            12: '[EW_MODE] CNC模式错误。',
            13: '[EW_REJECT] CNC拒绝执行。检查执行条件。',
            14: '[EW_DTSRVR] 数据服务器错误。',
            15: '[EW_ALARM] CNC报警，功能无法执行。请消除CNC警报。',
            16: '[EW_STOP] CNC停止或出现紧急状况。',
            17: '[EW_PASSWD] 数据被CNC保护。'
        }
        raise Exception("错误代码:{} {}".format(error_code, cnc_error_dic[error_code]))

    def __init__(self, ip, port=8193, win32=True):
        """
        初始化连接类，win32表示是否为windows系统
        """
        self.ip = ip
        self.port = port
        if win32:
            self.lib_so = windll.LoadLibrary('./fwlibe1.dll')
        else:
            self.lib_so = cdll.LoadLibrary('./libfwlib32-linux-x64.so')

        # 指定日志文件
        # self.lib_so.cnc_startupprocess.restype = c_short
        # ret = self.lib_so.cnc_startupprocess(0, "focas.log")
        # if ret:
        #     self.raise_error(ret)

    def connect(self):
        """
        连接到机床
        """
        if not self.is_open():
            # 参数配置
            self.lib_so.cnc_allclibhndl3.restype = c_short
            self.lib_so.cnc_allclibhndl3.argtypes = (c_char_p, c_ushort, c_long, POINTER(c_ushort))
            handle = c_ushort(0)

            # 连接机床
            ret = self.lib_so.cnc_allclibhndl3(bytes(self.ip, 'utf-8'), self.port, 10, byref(handle))
            if ret:
                CNC.raise_error(ret)

            self.__is_open = True
            CNC.__handle = handle

    def close(self):
        """
        关闭连接
        :return:
        """
        if self.is_open():
            self.__is_open = False
            self.lib_so.cnc_freelibhndl.restype = c_short
            self.lib_so.cnc_freelibhndl.argtypes = (c_ushort,)
            res = self.lib_so.cnc_freelibhndl(CNC.__handle)
            if res:
                CNC.raise_error(res)

    def is_open(self):
        return self.__is_open

    @classmethod
    def handle(cls):
        return cls.__handle
