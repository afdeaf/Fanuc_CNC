from ctypes import *

"""
MAX_AXIS F22_TYPE5 = 48
         F22_TYPEA = 72
         F22_TYPEB = 96
         否则为32
"""
MAX_AXIS = 32

"""
MAX_CNCPATH F22_TYPEA = 15
            否则为10
"""
MAX_CNCPATH = 10


# 结构体定义
class ODBAXIS(Structure):
    _fields_ = [("dummy", c_short),
                ("type", c_short),
                ("data", c_long * MAX_AXIS)]


# 结构体定义
class ODBACT(Structure):
    _fields_ = [('dummy', c_short * MAX_AXIS),
                ('data', c_long)]


# 结构体定义
class ODBACT2(Structure):
    _fields_ = [('datano', c_short),
                ('type', c_short),
                ('data', c_long * MAX_AXIS)]


# 结构体定义
class ODBCSS(Structure):
    _fields_ = [('srpm', c_long),  # 转换过的主轴转速
                ('sspm', c_long),  # 表面速度
                ('smax', c_long)]  # 最大转速时的钳位电压


class SPEEDELM(Structure):
    _fields_ = [('data', c_long),       # 速度数据
                ('dec', c_short),       # 小数点位置？
                ('unit', c_short),      # 单位 0:mm, 1:inch, 2:rpm,
                ('reserve', c_short),
                ('name', c_char),       # F:进给率, S:主轴速度
                ('suff', c_char)]


class ODBSPEED(Structure):
    _fields_ = [('actf', SPEEDELM),
                ('acts', SPEEDELM)]


class Path(Structure):
    _fields_ = [('system', c_short),        # 系统种类：0x204D代表machining，0x2054代表turning, 0x2057代表wirecut
                ('group', c_short),         # 系统组别，1代表 machining，2代表turning
                ('attrib', c_short),        # 路径属性：0表示CNC，1表示Loader
                ('ctrl_axis', c_short),     # 每个路径控制的轴数
                ('ctrl_srvo', c_short),     # 每个路径控制的伺服数
                ('ctrl_spdl', c_short),     # 每个路径的主轴
                ('mchn_no', c_short),       # 机器组号
                ('reserved', c_short)]      #


class ODBSYSEX(Structure):
    _fields_ = [('max_axis', c_short),      # 最大控制轴数
                ('max_spdl', c_short),      # 最大主轴数
                ('max_path', c_short),      # 最大路径数
                ('max_mchn', c_short),      # 最大加工组数
                ('ctrl_axis', c_short),     # 控制的轴数
                ('ctrl_srvo', c_short),     # 伺服轴数
                ('ctrl_spdl', c_short),     # 主轴数
                ('ctrl_path', c_short),     # 路径数
                ('ctrl_mchn', c_short),     # 组号
                ('reserved', c_short * 3),
                ('path', Path * MAX_CNCPATH)]  # 每个系统的信息存储在数组中


Alarm_info = {
    0: 'Parameter switch on	(SW)',
    1: 'Power off parameter set	(PW)',
    2: 'I/O error	(IO)',
    3: 'Foreground P/S	(PS)',
    4: 'Over travel, External data	(OT)',
    5: 'Overheat alarm	(OH)',
    6: 'Servo alarm	(SV)',
    7: 'Data I/O error	(SR)',
    8: 'Macro alarm	(MC)',
    9: 'Spindle alarm	(SP)',
    10: 'Other alarm(DS)	(DS)',
    11: 'Alarm concerning Malfunction prevent functions	(IE)',
    12: 'Background P/S	(BG)',
    13: 'Synchronized error	(SN)',
    14: '(reserved)	',
    15: 'External alarm message	(EX)',
    16: '(reserved)	',
    17: '(reserved)	',
    18: '(reserved)	',
    19: 'PMC error	(PC)',
}


class ODBTLIFE2(Structure):
    _fields_ = [('dummy', c_short * 2),
                ('data', c_long)]


class ODBTLIFE3(Structure):
    _fields_ = [('datano', c_short),
                ('dummy', c_short),
                ('data', c_long)]


class ODBTLUSE(Structure):
    _fields_ = [('s_grp', c_short),       # 组号起始位置
                ('dummy', c_short),       #
                ('e_grp', c_short),       # 组号结束位置,
                ('data', c_long)]         # data本来应该是一个e_grp - s_grp长的数组


class ODBUSEGRP(Structure):
    _fields_ = [('next', c_long),         #
                ('use', c_long),          #
                ('slct', c_long),         #
                ('opt_next', c_long),     #
                ('opt_use', c_long),      #
                ('opt_slct', c_long)]     #


# ODBNC开始
class BIN(Structure):
    _fields_ = [('reg_prg', c_short),         # 注册的程序总数
                ('unreg_prg', c_short),       # 可用程序数
                ('used_mem', c_long),         # 已使用内存
                ('unused_mem', c_long)]       # 未使用的内存


class U(Union):
    _fields_ = [('bin', BIN),             #
                ('asc', c_char * 31)]     #


class ODBNC(Structure):
    _fields_ = [('u', U)]     #
# ODBNC结束


class ODBPRO(Structure):
    _fields_ = [('dummy', c_short * 2),         # 未使用
                ('data', c_short),              # 正在执行的程序号
                ('mdata', c_short)]             # 主程序号


class ODBEXEPRG(Structure):
    _fields_ = [('name', c_char * 36),          # 程序名
                ('o_num', c_long)]              # 正在执行的程序号


# 时间结构体开始
class TIME(Structure):
    _fields_ = [('hour', c_short),
                ('minute', c_short),
                ('second', c_short)]


class DATE(Structure):
    _fields_ = [('year', c_short),
                ('month', c_short),
                ('date', c_short)]


class DATA(Union):
    _fields_ = [('date', DATE),
                ('time', TIME)]


class IODBTIMER(Structure):
    _fields_ = [('type', c_short),
                ('dummy', c_short),
                ('data', DATA)]
# 时间结构体结束


# 状态信息相关开始
class ODBST(Structure):
    _fields_ = [('dummy', c_short * 2),     # 未使用
                ('aut', c_short),           # 自动模式选择
                ('manual', c_short),        # 手动模式选择
                ('run', c_short),           # 自动模式的状态
                ('edit', c_short),          # 程序编辑状态
                ('motion', c_short),        # 轴的动作状态，移动/停止
                ('mstb', c_short),          # M,S,T,B功能的状态
                ('emergency', c_short),     # 紧急状态
                ('write', c_short),         # 写入备份内存的状态
                ('labelskip', c_short),     #
                ('alarm', c_short),         # 报警状态
                ('warning', c_short),       # 警告状态
                ('battery', c_short)]       # 电池状态


AUT = {
    0: '未选择',
    1: 'MDI',
    2: 'TAPE(Series 15), DNC(Series 15i)',
    3: 'MEMory',
    4: 'EDIT',
    5: 'TeacHIN',
}

MANUAL = {
    0:	'未选择',
    1:	'REFerence',
    2:	'INC·feed',
    3:	'HaNDle',
    4:	'JOG',
    5:	'AnGularJog',
    6:	'Inc+Handl',
    7:	'Jog+Handl'
}

RUN = {
    0:	'停止',
    1:	'等待',
    2:	'开始',
    3:	'MSTR(jog mdi)',
    4:	'ReSTaRt(not blinking)',
    5:	'PRSR(program restart)',
    6:	'NSRC(sequence number search)',
    7:	'ReSTaRt(blinking)',
    8:	'ReSET',
    13:	'HPCC(during RISC operation)'
}

MOTION = {
    1:	'正在移动',
    2:	'停止',
    3:	'等待'
}

EMERGENCY = {
    0:	'处于非紧急状态',
    1:	'处于紧急状态'
}
# 状态信息结束
