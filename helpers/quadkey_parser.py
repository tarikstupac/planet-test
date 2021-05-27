from ctypes import c_char, c_ulonglong, c_ulong, create_string_buffer

def quadkey_to_quadint(quadkey):
    zoom : int = len(quadkey)
    qi = c_ulonglong(0)
    bit_loc = c_ulong()

    for i in range(zoom):
        bit_loc = c_ulong(64-((i+1) * 2))
        qi = c_ulonglong(qi.value | (int(quadkey[i]) << bit_loc.value))
    qi = c_ulonglong(qi.value | zoom)

    return qi.value

def quadint_to_quadkey(quadint):
    qi = c_ulonglong(quadint)
    zoom = int(quadint) & 0b11111
    qk = create_string_buffer(31)

    for i in range(zoom):
        bit_loc = (64 - ((i + 1) * 2))
        char_bits = c_ulong((qi.value & (0b11 << bit_loc)) >> bit_loc)
        qk[i]= c_char(ord(str(char_bits.value)))

    return qk[:zoom].decode('UTF-8')
