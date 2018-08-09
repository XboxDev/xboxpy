from .interface import api
from . import pe
import struct

SCSI_IOCTL_DATA_OUT         = 0
SCSI_IOCTL_DATA_IN          = 1
SCSI_IOCTL_DATA_UNSPECIFIED = 2

IOCTL_SCSI_PASS_THROUGH        = 0x4D004
IOCTL_SCSI_PASS_THROUGH_DIRECT = 0x4D014

PAGE_READWRITE = 0x04

NULL = 0

FALSE = 0x00000000
TRUE  = 0x00000001 # FIXME: Check if these are correct!

HalHaltRoutine = 0
HalRebootRoutine = 1
HalQuickRebootRoutine = 2
HalKdRebootRoutine = 3
HalFatalErrorRebootRoutine = 4

def AvSendTVEncoderOption(RegisterBase, Option, Param, Result):
  #IN PVOID RegisterBase,
  #IN ULONG Option,
  #IN ULONG Param,
  #OUT PULONG Result
  call_stdcall(2, "<IIII", RegisterBase, Option, Param, Result)

def HalReadSMBusValue(SlaveAddress, CommandCode, ReadWordValue, DataValue):
  #IN UCHAR SlaveAddress,
  #IN UCHAR CommandCode,
  #IN BOOLEAN ReadWordValue,
  #OUT ULONG *DataValue
  return call_stdcall(45, "<IIII", SlaveAddress, CommandCode, ReadWordValue, DataValue)

def HalReadWritePCISpace(BusNumber, SlotNumber, RegisterNumber, Buffer, Length, WritePCISpace):
  #IN ULONG BusNumber,
  #IN ULONG SlotNumber,
  #IN ULONG RegisterNumber,
  #IN PVOID Buffer,
  #IN ULONG Length,
  #IN BOOLEAN WritePCISpace
  call_stdcall(46, "<IIIIII", BusNumber, SlotNumber, RegisterNumber, Buffer, Length, WritePCISpace)

def HalReturnToFirmware(Routine):
  #FIRMWARE_REENTRY Routine
  call_stdcall(49, "<I", Routine)

def HalWriteSMBusValue(SlaveAddress, CommandCode, WriteWordValue, DataValue):
  #IN UCHAR SlaveAddress,
  #IN UCHAR CommandCode,
  #IN BOOLEAN WriteWordValue,
  #IN ULONG DataValue
  return call_stdcall(50, "<IIII", SlaveAddress, CommandCode, WriteWordValue, DataValue)

def IoDeviceObjectType():
  return pe.resolve_export(70)

def IoSynchronousDeviceIoControlRequest(IoControlCode, DeviceObject, InputBuffer, InputBufferLength, OutputBuffer, OutputBufferLength, ReturnedOutputBufferLength, InternalDeviceIoControl):
  #IN ULONG IoControlCode,
  #IN PDEVICE_OBJECT DeviceObject,
  #IN PVOID InputBuffer OPTIONAL,
  #IN ULONG InputBufferLength,
  #OUT PVOID OutputBuffer OPTIONAL,
  #IN ULONG OutputBufferLength,
  #OUT PULONG ReturnedOutputBufferLength OPTIONAL,
  #IN BOOLEAN InternalDeviceIoControl) # FIXME: How to handle this one properly? xxxB? Bxxx? I?
  return call_stdcall(84, "<IIIIIIII", IoControlCode, DeviceObject, InputBuffer, InputBufferLength, OutputBuffer, OutputBufferLength, ReturnedOutputBufferLength, InternalDeviceIoControl)

def KeTickCount():
  return pe.resolve_export(156)

def LaunchDataPage():
  return pe.resolve_export(164)

def MmAllocateContiguousMemory(NumberOfBytes):
  return call_stdcall(165, "<I", NumberOfBytes)

def MmAllocateContiguousMemoryEx(NumberOfBytes, LowestAcceptableAddress, HighestAcceptableAddress, Alignment, Protect):
  return call_stdcall(166, "<IIIII", NumberOfBytes, LowestAcceptableAddress, HighestAcceptableAddress, Alignment, Protect)

def MmFreeContiguousMemory(BaseAddress):
  return call_stdcall(171, "<I", BaseAddress)

def MmGetPhysicalAddress(BaseAddress):
  return call_stdcall(173, "<I", BaseAddress)

def MmMapIoSpace(PhysicalAddress, NumberOfBytes, Protect):
  #IN ULONG_PTR PhysicalAddress,
  #IN SIZE_T NumberOfBytes,
  #IN ULONG Protect
  return call_stdcall(177, "<III", PhysicalAddress, NumberOfBytes, Protect)

def MmPersistContiguousMemory(BaseAddress, NumberOfBytes, Persist):
  #IN PVOID BaseAddress,
  #IN SIZE_T NumberOfBytes,
  #IN BOOLEAN Persist
  return call_stdcall(178, "<III", BaseAddress, NumberOfBytes, Persist)

def MmSetAddressProtect(BaseAddress, NumberOfBytes, NewProtect):
  #IN PVOID BaseAddress,
  #IN ULONG NumberOfBytes,
  #IN ULONG NewProtect
  call_stdcall(182, "<III", BaseAddress, NumberOfBytes, NewProtect)

def MmUnmapIoSpace(BaseAddress, NumberOfBytes):
  #IN PVOID BaseAddress,
  #IN SIZE_T NumberOfBytes,
  return call_stdcall(183, "<II", BaseAddress, NumberOfBytes)

def ObReferenceObjectByName(ObjectName, Attributes, ObjectType, ParseContext, Object):
  #IN POBJECT_STRING ObjectName,
  #IN ULONG Attributes,
  #IN POBJECT_TYPE ObjectType,
  #IN OUT PVOID ParseContext OPTIONAL,
  #OUT PVOID *Object
  return call_stdcall(247, "<IIIII", ObjectName, Attributes, ObjectType, ParseContext, Object)

def RtlInitAnsiString(DestinationString, SourceString):
  #IN OUT PANSI_STRING DestinationString,
  #IN PCSZ SourceString
  return call_stdcall(289, "<II", DestinationString, SourceString)

def XboxEEPROMKey():
  return pe.resolve_export(321)

def XboxHDKey():
  return pe.resolve_export(323)

def XboxSignatureKey():
  return pe.resolve_export(325)

def XeImageFileName():
  return pe.resolve_export(326)

def READ_PORT_BUFFER_UCHAR(Port, Buffer, Count):
  #PUCHAR Port,
  #PUCHAR Buffer,
  #ULONG Count
  call_stdcall(329, "<III", Port, Buffer, Count)

def READ_PORT_BUFFER_USHORT(Port, Buffer, Count):
  #PUSHORT Port,
  #PUSHORT Buffer,
  #ULONG Count
  call_stdcall(330, "<III", Port, Buffer, Count)

def READ_PORT_BUFFER_ULONG(Port, Buffer, Count):
  #PULONG Port,
  #PULONG Buffer,
  #ULONG Count
  call_stdcall(331, "<III", Port, Buffer, Count)

def WRITE_PORT_BUFFER_UCHAR(Port, Buffer, Count):
  #IN PUCHAR Port,
  #IN PUCHAR Buffer,
  #IN ULONG Count
  call_stdcall(332, "<III", Port, Buffer, Count)

def WRITE_PORT_BUFFER_USHORT(Port, Buffer, Count):
  #IN PUSHORT Port,
  #IN PUSHORT Buffer,
  #IN ULONG Count
  call_stdcall(333, "<III", Port, Buffer, Count)

def WRITE_PORT_BUFFER_ULONG(Port, Buffer, Count):
  #IN PULONG Port,
  #IN PULONG Buffer,
  #IN ULONG Count
  call_stdcall(334, "<III", Port, Buffer, Count)

def XboxLANKey():
  return pe.resolve_export(353)

def XboxAlternateSignatureKeys():
  return pe.resolve_export(354)

def XePublicKeyData():
  return pe.resolve_export(355)

def call_stdcall(function, types, *arguments):
  address = pe.resolve_export(function)
  registers = api.call(address, struct.pack(types, *arguments))
  return registers['eax']
