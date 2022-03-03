from . import api
from . import get_xbox_address
import socket
import struct
import os
import sys
import time
import importlib

(HOST, PORT) = get_xbox_address(731)
connection_timeout = 0.5


xbdm = None

def xbdm_read_line():
  data = b''
  while True:
    #print("Waiting")
    byte = xbdm.recv(1)
    #print("Got " + str(byte))
    if byte == b'\r':
      byte = xbdm.recv(1)
      assert(byte == b'\n')
      break
    data += byte
  return data

def xbdm_parse_response(length=None):
  try:
    res = xbdm_read_line()
    if res[3] != ord('-'):
      raise
    status = int(res[0:3])
    if res[4] != ord(' '):
      raise
    res = res[5:]
  except:
    return (None, None)

  if status == 200:
    return (status, str(res, encoding='ascii'))

  elif status == 201:
    return (status, str(res, encoding='ascii'))

  elif status == 202:
    lines = []
    while True:
      line = xbdm_read_line()
      if line == b'.': #end of response
        break
      lines += [str(line, encoding='ascii')]
    return (status, lines)

  elif status == 203:
    res = bytearray()

    # This will not work with most commands, but "getfile" prefixes the
    # transfer with the actual length, so we need to support it.
    if length == 0:
      length = struct.unpack("<I", xbdm.recv(4))[0]

    assert(length != None)
    while True:
      remaining = length - len(res)
      if remaining == 0:
        break
      assert(remaining > 0)
      res += xbdm.recv(remaining)
    return (status, bytes(res))

  elif status == 204:
    return (status, str(res, encoding='ascii'))

  else:
    print("Unknown status: " + str(status))
    print("from response: " + str(res))
    #FIXME: Read remaining buffer?!

  return (status, res)

def xbdm_command(cmd, data=None, length=None):
  #FIXME: If type is already in bytes we just send it binary!
  #print("Running '" + cmd + "'")
  xbdm.sendall(bytes(cmd + "\r\n", encoding='ascii'))
  #print("Sent")
  status, lines = xbdm_parse_response(length)

  # Respond with requested data
  if status == 204:
    xbdm.sendall(data)
    status, lines = xbdm_parse_response()

  #print("Done")
  return status, lines

import re

def xbdm_parse_keys(string):

  #FIXME: Rewrite this function to work without `re`

  result = dict(re.findall(r'(\S+)=(".*?"|\S+)', string))

  # Clean up datatypes
  for key in result:
    if result[key][0:2] == '0x':
      result[key] = int(result[key][2:], 16)
    elif result[key][0] == '\"' and result[key][-1] == '\"':
      #FIXME: Unescape strings?
      result[key] = result[key].strip('"')
    else:
      assert(False)

  # There might be keys without values (tags), so we add those now
  tags = re.findall(r'(\S+)(?![^=])', string)
  for tag in tags:
    if tag not in result:
      result[tag] = True

  return result

def GetModules():
  modulesList = []
  status, lines = xbdm_command("modules")

  for line in lines:
    module = xbdm_parse_keys(line)
    modulesList.append(module)

  print(modulesList)
  return modulesList

def GetMem(addr, length):
  if length == 0:
    return bytes([])
  if False:
    cmd = "getmem addr=0x" + format(addr, 'X') + " length=0x" + format(length, 'X')
    status, lines = xbdm_command(cmd)
    data = bytearray()
    for line in lines:
      line = str(line, encoding='ascii').strip()
      for i in range(0, len(line) // 2):
        byte = line[i*2+0:i*2+2]
        if '?' in byte:
          print("Oops?!")
          byte = '00'
        data.append(int(byte,16))
    assert(len(data) == length)
  else:
    cmd = "getmem2 addr=0x" + format(addr, 'X') + " length=0x" + format(length, 'X')
    status, data = xbdm_command(cmd, length=length)
  return bytes(data)

def SetMem(addr, data):
  value = bytes(data)

  # Unfortunately XBDM has a maximum line-buffer of about ~500 symbols.
  # We'll be conservative and only allow 200 bytes (400 hex digits).
  # That leaves ~100 bytes for the actual command.
  max_len = 200
  if len(value) > max_len:
    SetMem(addr, value[0:max_len])
    SetMem(addr + max_len, value[max_len:])
  else:
    cmd="setmem addr=0x" + format(addr, 'X') + " data="
    for i in range(0, len(value)):
      cmd += format(value[i], '02X')
    xbdm_command(cmd)


def delay_retry(reason):
  print(reason + ". Retrying in " + str(int(1000 * connection_timeout)) + " ms")
  time.sleep(connection_timeout)
  print("Retrying now")

def connect():
  global xbdm
  # Repeat until we are fully connected
  while True:
    # Wait until we get a connection
    while True:
      if xbdm != None:
        xbdm.close()
      try:
        xbdm = socket.create_connection((HOST, PORT), timeout=connection_timeout)
        break
      except socket.timeout:
        print("Connection timeout. Retrying")
      except socket.gaierror as err:
        sys.exit("Connection error: '" + str(err) + "'")
      except ConnectionRefusedError:
        delay_retry("Connection refused")
      except:
        sys.exit("Unknown connection error")
    # Get login message
    try:
      status, data = xbdm_parse_response()
      if status == None:
        raise
      if status != 201:
        delay_retry("Bad status " + str(status) + ", expected 201")
        continue
    except:
      delay_retry("Could not get expected response")
      continue
    # Leave the loop, we are connected!
    break

print("Connecting to '" + HOST + "' (Port " + str(PORT) + ")")
connect()


# Used during bootstrap only!

def read1(address, size, physical):
  assert(physical == False);
  return GetMem(address, size)
def write1(address, data, physical):
  assert(physical == False);
  return SetMem(address, data)

api.read = read1
api.write = write1

# Hack some functions so we have better read/write access
# See xbdm-hack.md for more information

hacked = False
if True:

  from xboxpy.pe import *

  modules=GetModules()
  xbdm_module = [module for module in modules if module['name'] == "xbdm.dll"][0]
  xbdm_base = xbdm_module['base']
  DmResumeThread_addr = resolve_export(35, image_base=xbdm_base)

  hack = "0F20C05025FFFFFEFF0F22C08B5424088B1A8B4A048B4208E2028A03E203668B03E2028B03E2028803E203668903E2028903E21F6089250000018089C129CC89E78D720CF3A4FFD38B25000001808944241C61894208580F22C0B80000DB02C2040090909090"
  xbdm_command("setmem addr=0x" + format(DmResumeThread_addr, 'X') + " data=" + hack)

  #hack_bank = DmResumeThread_addr + (len(hack) // 2) # Put communication base behind the hack code [pretty shitty..]
  hack_bank = xbdm_base # Overwrite xbdm PE header
  #hack_bank = 0xd0032FC0 # Works on console ?
  #hack_bank = 0xD004E000 - 12 # Top of stack - works in XQEMU?!

  hacked = True
  print("Hack installed, bank at 0x" + format(hack_bank, '08X'))

def xbdm_hack(address, operation, data=0):
  SetMem(hack_bank, struct.pack("<III", address, operation, data))
  xbdm_command("resume thread=0x" + format(hack_bank, 'X'))
  return GetMem(hack_bank + 8, 4)

def xbdm_read_8(address):
  return xbdm_hack(address, 1)
def xbdm_read_16(address):
  return xbdm_hack(address, 2)
def xbdm_read_32(address):
  return xbdm_hack(address, 3)

def xbdm_write_8(address, data):
  xbdm_hack(address, 4, int.from_bytes(data, byteorder='little', signed=False))
def xbdm_write_16(address, data):
  xbdm_hack(address, 5, int.from_bytes(data, byteorder='little', signed=False))
def xbdm_write_32(address, data):
  xbdm_hack(address, 6, int.from_bytes(data, byteorder='little', signed=False))

def xbdm_call(address, stack):
  assert(len(stack) < 64)
  SetMem(hack_bank + 12, stack)
  return xbdm_hack(address, 7, len(stack))

def read2(address, size, physical):
  if physical:
    assert(False)
  if hacked:
    if size == 1:
      return xbdm_read_8(address)[0:1]
    if size == 2:
      return xbdm_read_16(address)[0:2]
    if size == 4:
      return xbdm_read_32(address)[0:4]
  return GetMem(address, size)
def write2(address, data, physical):
  if physical:
    assert(False)
  if hacked:
    size = len(data)
    if size == 1:
      return xbdm_write_8(address, data)
    if size == 2:
      return xbdm_write_16(address, data)
    if size == 4:
      return xbdm_write_32(address, data)
  return SetMem(address, data)


def call(address, stack, registers=None):
  assert(registers == None)
  eax_bytes = xbdm_call(address, stack)
  out_registers = {}
  out_registers['eax'] = int.from_bytes(eax_bytes, byteorder='little', signed=False)
  return out_registers

api.read = read2
api.write = write2
api.call = call
