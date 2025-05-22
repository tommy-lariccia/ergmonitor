class CSafeParser:
    ...



















def make_standard_frame():
    frame = bytearray([0xF1])
    contents = _get_frame_contents()
    frame.extend(contents)
    frame.append(_get_checksum(contents))
    frame.append(0xF2)
    return bytes(frame)


def _get_frame_contents() -> bytearray:
    contents = bytearray()
    contents.append(0xAB)
    return contents


def _get_checksum(contents: bytearray) -> int:
    checksum = contents[0]
    for byte in contents[1:]:
        checksum ^= byte
    return checksum


#make_standard_frame()
