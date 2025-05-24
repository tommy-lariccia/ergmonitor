from .csafe_config import (STANDARD_FRAME_START_FLAG, STOP_FLAG,
                           BYTE_STUFFING_MAP, BYTE_STUFFING_FLAG, MAX_FRAME_LENGTH)


def is_valid_command(ident: str) -> bool:
    return True
    #return ident in csafe_com_schematics


def is_public_command(ident: str) -> bool:
    return not is_private_command(ident)


def is_private_command(ident: str) -> bool:
    return ident.startswith('CSAFE_PM_')


def is_short_command(ident: str) -> bool:
    return True
    # return not len(csafe_com_schematics[ident]['cargs'])


def _make_short_command(ident: int) -> bytes:
    buffer = bytearray()
    buffer.append(ident)
    # buffer.append(csafe_com_schematics[ident]['com_id'])
    return bytes(buffer)


def make_command(ident: int) -> bytes:
    if is_short_command(ident):
        return _make_short_command(ident)


def _make_checksum(contents: bytes | bytearray) -> int:
    checksum = 0x00
    for byte in contents:
        checksum ^= byte
    return checksum


def _make_byte_stuffed(fbuffer: bytes | bytearray) -> bytes:
    buffer = bytearray()
    for byte in fbuffer:
        if byte in BYTE_STUFFING_MAP:
            buffer.extend([BYTE_STUFFING_FLAG, BYTE_STUFFING_MAP[byte]])
        else:
            buffer.append(byte)
    return bytes(buffer)


def make_standard_frame(contents: bytes | bytearray) -> bytes:
    if not len(contents):
        return bytes(bytearray([STANDARD_FRAME_START_FLAG, STOP_FLAG]))
    buffer = bytearray()
    buffer.append(STANDARD_FRAME_START_FLAG)
    contents = bytearray(contents)
    contents.append(_make_checksum(contents))
    contents = _make_byte_stuffed(contents)
    buffer.extend(contents)
    buffer.append(STOP_FLAG)
    return bytes(buffer)


def is_within_size_limits(frame: bytes) -> bool:
    return len(frame) <= MAX_FRAME_LENGTH


def read_results(ident: str, fdata: bytearray | bytes):
    assert fdata[0] == STANDARD_FRAME_START_FLAG
    assert fdata[-1] == STOP_FLAG
    status = fdata[1]
    contents = fdata[2:-1]
    print(contents)
    ...


if __name__ == '__main__':
    # print(make_standard_frame(b'\xab\x91'))
    read_results('CSAFE_GETUSERINFO_CMD', b'\xf1\x01\xab\x05\x19\x03\x28\x00\x00\x9d\xf2')
