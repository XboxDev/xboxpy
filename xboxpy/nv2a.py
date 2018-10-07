from . import memory

def read_u8(address):
  return memory.read_u8(0xFD000000 + address)
def read_u16(address):
  return memory.read_u16(0xFD000000 + address)
def read_u32(address):
  return memory.read_u32(0xFD000000 + address)

def write_u8(address, value):
  memory.write_u8(0xFD000000 + address, value)
def write_u16(address, value):
  memory.write_u16(0xFD000000 + address, value)
def write_u32(address, value):
  memory.write_u32(0xFD000000 + address, value)

def ReadCRTC(i):
  write_u8(0x6013D4, i)
  return read_u8(0x6013D5)

#FIXME: Swizzler ported from XQEMU.. does not work - WHY?!

def GenerateSwizzleMask(size):
  bit = 1
  mask_bit = 1
  x = 0
  y = 0
  z = 0
  done = False
  while not done:
    done = True
    if bit < size[0]:
      x |= mask_bit
      mask_bit <<= 1
      done = False
    if bit < size[1]:
      y |= mask_bit
      mask_bit <<= 1
      done = False
    if bit < size[2]:
      z |= mask_bit
      mask_bit <<= 1
      done = False
    bit <<= 1
  assert(x ^ y ^ z == (mask_bit - 1))
  return (x, y, z)

# This fills a pattern with a value if your value has bits abcd and your
# pattern is 11010100100 this will return: 0a0b0c00d00
def _FillPattern(pattern, value):
  result = 0
  bit = 1
  while value > 0:
    if (pattern & bit):
      result |= bit if (value & 1) else 0
      value >>= 1
    bit <<= 1
  return result

def GetSwizzledOffset(offset, mask, bits_per_pixel):
  assert(bits_per_pixel % 8 == 0)
  new_offset  = _FillPattern(mask[0], offset[0])
  new_offset |= _FillPattern(mask[1], offset[1])
  new_offset |= _FillPattern(mask[2], offset[2])
  return (bits_per_pixel // 8) * new_offset

def Swizzle():
  assert(False)

def Unswizzle(data, bits_per_pixel, size, pitch):
  assert(bits_per_pixel % 8 == 0)
  bytes_per_pixel = bits_per_pixel // 8

  if len(size) == 2:
    size = (size[0], size[1], 1)
    pitch = (pitch, 0)
  elif len(size) == 3:
    assert(len(pitch) == 2)
  else:
    assert(False) # Unknown size

  data = bytes(data)
  unswizzled = bytearray([0] * len(data))

  #print(size)
  mask = GenerateSwizzleMask(size)
  #print(bin(mask[0]).rjust(34))
  #print(bin(mask[1]).rjust(34))
  #print(bin(mask[2]).rjust(34))

  for z in range(0, size[2]):
    for y in range(0, size[1]):
      for x in range(0, size[0]):
        src = GetSwizzledOffset((x, y, z), mask, bits_per_pixel)
        dst = z * pitch[1] + y * pitch[0] + x * bytes_per_pixel

        for i in range(0, bytes_per_pixel):
          b = data[src+i]
          unswizzled[dst+i] = b
        #unswizzled[dst:dst + bytes_per_pixel] = data[src:src + bytes_per_pixel]

  return bytes(unswizzled)
