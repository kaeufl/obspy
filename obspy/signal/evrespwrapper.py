import numpy as np
import ctypes as C
from obspy.signal.headers import clibevresp

clibevresp.twoPi = 3.141

ENUM_UNITS = {
    "UNDEF_UNITS": 0,
    "DIS": 1,
    "VEL": 2,
    "ACC": 3,
    "COUNTS": 4,
    "VOLTS": 5,
    "DEFAULT": 6,
    "PRESSURE": 7,
    "TESLA": 8
}

ENUM_FILT_TYPES = {
    "UNDEF_FILT": 0,
    "LAPLACE_PZ": 1,
    "ANALOG_PZ": 2,
    "IIR_PZ": 3,
    "FIR_SYM_1": 4,
    "FIR_SYM_2": 5,
    "FIR_ASYM": 6,
    "LIST": 7,
    "GENERIC": 8,
    "DECIMATION": 9,
    "GAIN": 10,
    "REFERENCE": 11,
    "FIR_COEFFS": 12,
    "IIR_COEFFS": 13
}


ENUM_STAGE_TYPES = {
    "UNDEF_STAGE": 0,
    "PZ_TYPE": 1,
    "IIR_TYPE": 2,
    "FIR_TYPE": 3,
    "GAIN_TYPE": 4,
    "LIST_TYPE": 5,
    "IIR_COEFFS_TYPE": 6,
    "GENERIC_TYPE": 7
}


class complex_number(C.Structure):
    _fields_ = [
        ("real", C.c_double),
        ("imag", C.c_double),
    ]


class pole_zeroType(C.Structure):
    _fields_ = [
        ("nzeros", C.c_int),
        ("npoles", C.c_int),
        ("a0", C.c_double),
        ("a0_freq", C.c_double),
        ("zeros", C.POINTER(complex_number)),
        ("poles", C.POINTER(complex_number)),
    ]


class coeffType(C.Structure):
    _fields_ = [
    ]


class firType(C.Structure):
    _fields_ = [
    ]


class listType(C.Structure):
    _fields_ = [
    ]


class genericType(C.Structure):
    _fields_ = [
    ]


class decimationType(C.Structure):
    _fields_ = [
    ]


class decimationType(C.Structure):
    _fields_ = [
    ]


class gainType(C.Structure):
    _fields_ = [
    ]


class referType(C.Structure):
    _fields_ = [
    ]


class blkt_info_union(C.Union):
    _fields_ = [
        ("pole_zero", pole_zeroType)
    ]


class blkt(C.Structure):
    pass

blkt._fields_ = [
    ("type", C.c_int),
    ("blkt_info", blkt_info_union),
    #("blkt_info", pole_zeroType),
    ("next_blkt", C.POINTER(blkt))
]


class stage(C.Structure):
    pass

stage._fields_ = [
    ("sequence_no", C.c_int),
    ("input_units", C.c_int),
    ("output_units", C.c_int),
    ("first_blkt", C.POINTER(blkt)),
    ("next_stage", C.POINTER(stage))
]

STALEN = 64
NETLEN = 64
LOCIDLEN = 64
CHALEN = 64
DATIMLEN = 23
MAXLINELEN = 256

# needed ?
OUTPUTLEN = 256
TMPSTRLEN = 64
UNITS_STR_LEN = 16
UNITSLEN = 20
BLKTSTRLEN = 4
FLDSTRLEN = 3
MAXFLDLEN = 50
MAXLINELEN = 256
FIR_NORM_TOL = 0.02


class channel(C.Structure):
    pass

channel._fields_ = [
    ("staname", C.c_char * STALEN),
    ("network", C.c_char * NETLEN),
    ("locid", C.c_char * LOCIDLEN),
    ("chaname", C.c_char * CHALEN),
    ("beg_t", C.c_char * DATIMLEN),
    ("end_t", C.c_char * DATIMLEN),
    ("first_units", C.c_char * MAXLINELEN),
    ("last_units", C.c_char * MAXLINELEN),
    ("sensit", C.c_double),
    ("sensfreq", C.c_double),
    ("calc_sensit", C.c_double),
    ("calc_delay", C.c_double),
    ("estim_delay", C.c_double),
    ("applied_corr", C.c_double),
    ("sint", C.c_double),
    ("nstages", C.c_int),
    ("first_stage", C.POINTER(stage)),
]


# void calc_resp(struct channel *chan, double *freq, int nfreqs,
#                struct complex *output,
#                char *out_units, int start_stage, int stop_stage,
#                int useTotalSensitivityFlag)
clibevresp.calc_resp.argtypes = [
    C.POINTER(channel),
    np.ctypeslib.ndpointer(dtype='float64',  # freqs
                           ndim=1,
                           flags='C_CONTIGUOUS'),
    C.c_int,
    np.ctypeslib.ndpointer(dtype='complex128',  # output
                           ndim=1,
                           flags='C_CONTIGUOUS'),
    C.c_char_p,
    C.c_int,
    C.c_int,
    C.c_int]
clibevresp.calc_resp.restype = C.c_void_p