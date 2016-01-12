import zlib
def encode(s):
    #obj = zlib.compressobj(9, zlib.DEFLATED, 8, zlib.DEF_MEM_LEVEL, 0)
    encoding = zlib.compress(s, 9)
    return encoding
