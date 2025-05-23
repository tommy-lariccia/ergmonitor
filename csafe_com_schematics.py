import json

BYTE_STUFFING_MAP = {0xF0: 0x00,
                     0xF1: 0x01,
                     0xF2: 0x02,
                     0xF3: 0x03}

EXTENDED_FRAME_START_FLAG = 0xF0
STANDARD_FRAME_START_FLAG = 0xF1
STOP_FLAG = 0xF2
BYTE_STUFFING_FLAG = 0xF3

MAX_FRAME_LENGTH = 120

f = open('csafe_com_schematics.json', 'r')
csafe_com_schematics = json.loads(f.read())['commands']

for command in csafe_com_schematics:
    csafe_com_schematics[command]['com_id'] = int(csafe_com_schematics[command]['com_id'][2:], 16)

f.close()
