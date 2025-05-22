from typing import List


class Argument:
    def __init__(self, name: str, bsize: int, fbtype: str = "LS"):
        self.name = name
        self.bsize = bsize
        self._fbtype = fbtype


class Command:
    def __init__(self, name: str, cid: int, com_args: List[Argument], resp_args: List[Argument]):
        self.name = name
        self.cid = cid
        self.com_args = com_args
        self.resp_args = resp_args



# Public Short Commands
CSAFE_GETSTATUS_CMD = Command('CSAFE_GETSTATUS_CMD', 0x80, [],
                              [Argument("status", 1)])
CSAFE_RESET_CMD = Command('CSAFE_RESET_CMD', 0x81, [], [])
CSAFE_GOIDLE_CMD = Command('CSAFE_GOIDLE_CMD', 0x82, [], [])
CSAFE_GOHAVEID_CMD = Command('CSAFE_GOHAVEID_CMD', 0x83, [], [])
CSAFE_GOINUSE_CMD = Command('CSAFE_GOINUSE_CMD', 0x85, [], [])
CSAFE_GOFINISHED_CMD = Command('CSAFE_GOFINISHED_CMD', 0x86, [], [])
CSAFE_GOREADY_CMD = Command('CSAFE_GOREADY_CMD', 0x87, [], [])
CSAFE_BADID_CMD = Command('CSAFE_BADID_CMD', 0x88, [], [])
CSAFE_GETVERSION_CMD = Command('CSAFE_GETVERSION_CMD', 0x91, [], [Argument('mfg id', 1),
                                                                  Argument('cid', 1),
                                                                  Argument('model', 1),
                                                                  Argument('hw version', 2),
                                                                  Argument('sw version', 2))])
CSAFE_GETID_CMD = Command('CSAFE_GETID_CMD', 0x92, [], [])  # TODO
CSAFE_GETUNITS_CMD = Command('CSAFE_GETUNITS_CMD', 0x93, [], [])
CSAFE_GETSERIAL_CMD = Command('CSAFE_GETSERIAL_CMD', 0x94, [], [])
CSAFE_GETODOMETER_CMD = Command('CSAFE_GETODOMETER_CMD', 0x9B, [], [])
CSAFE_GETERRORCODE_CMD = Command('CSAFE_GETERRORCODE_CMD', 0x9C, [], [])
CSAFE_GETTWORK_CMD = Command('CSAFE_GETTWORK_CMD', 0xA0, [], [])
CSAFE_GETHORIZONTAL_CMD = Command('CSAFE_GETHORIZONTAL_CMD', 0xA1, [], [])
CSAFE_GETVERTICAL_CMD = Command('CSAFE_GETVERTICAL_CMD', 0xA2, [], [])
CSAFE_GETCALORIES_CMD = Command('CSAFE_GETCALORIES_CMD', 0xA3, [], [])
CSAFE_GETPROGRAM_CMD = Command('CSAFE_GETPROGRAM_CMD', 0xA4, [], [])
CSAFE_GETSPEED_CMD = Command('CSAFE_GETSPEED_CMD', 0xA5, [], [])
CSAFE_GETPACE_CMD = Command('CSAFE_GETPACE_CMD', 0xA6, [], [])
CSAFE_GETCADENCE_CMD = Command('CSAFE_GETCADENCE_CMD', 0xA7, [], [])
CSAFE_GETUSERINFO_CMD = Command('CSAFE_GETUSERINFO_CMD', 0xAB, [], [])
CSAFE_GETHRCUR_CMD = Command('CSAFE_GETHRCUR_CMD', 0xB0, [], [])
CSAFE_GETPOWER_CMD = Command('CSAFE_GETPOWER_CMD', 0xB4, [], [])
