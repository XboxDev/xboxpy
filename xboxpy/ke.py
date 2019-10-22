from .interface import api
from . import pe
import struct

SCSI_IOCTL_DATA_OUT         = 0
SCSI_IOCTL_DATA_IN          = 1
SCSI_IOCTL_DATA_UNSPECIFIED = 2

IOCTL_SCSI_PASS_THROUGH        = 0x4D004
IOCTL_SCSI_PASS_THROUGH_DIRECT = 0x4D014

PAGE_READONLY = 0x02
PAGE_READWRITE = 0x04
PAGE_NOCACHE = 0x200

MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000

NULL = 0

FALSE = 0x00000000
TRUE  = 0x00000001 # FIXME: Check if these are correct!

HalHaltRoutine = 0
HalRebootRoutine = 1
HalQuickRebootRoutine = 2
HalKdRebootRoutine = 3
HalFatalErrorRebootRoutine = 4

SYNCHRONIZE = 0x00100000
STANDARD_RIGHTS_REQUIRED = 0x000F0000

FileBasicInformation = 4
FileNetworkOpenInformation = 34

FILE_SHARE_READ = 1
FILE_SHARE_WRITE = 2

FILE_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0x1FF)


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

def HalRegisterShutdownNotification(ShutdownRegistration, Register):
  #IN PHAL_SHUTDOWN_REGISTRATION ShutdownRegistration,
  #IN BOOLEAN Register
  call_stdcall(47, "<II", ShutdownRegistration, Register)

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

def NtAllocateVirtualMemory(BaseAddress, ZeroBits, RegionSize, AllocationType, Protect):
  #IN OUT PVOID *BaseAddress,
  #IN ULONG_PTR ZeroBits,
  #IN OUT PSIZE_T RegionSize,
  #IN ULONG AllocationType,
  #IN ULONG Protect
  return call_stdcall(184, "<IIIII", BaseAddress, ZeroBits, RegionSize, AllocationType, Protect)

def NtClose(Handle):
  # IN HANDLE Handle
  return call_stdcall(187, "<I", Handle)

def NtOpenFile(FileHandle, DesiredAccess, ObjectAttributes, IoStatusBlock, ShareAccess, OpenOptions):
  #OUT PHANDLE FileHandle,
  #IN ACCESS_MASK DesiredAccess,
  #IN POBJECT_ATTRIBUTES ObjectAttributes,
  #OUT PIO_STATUS_BLOCK IoStatusBlock,
  #IN ULONG ShareAccess,
  #IN ULONG OpenOptions
  return call_stdcall(202, "<IIIIII", FileHandle, DesiredAccess, ObjectAttributes, IoStatusBlock, ShareAccess, OpenOptions)

def NtQueryInformationFile(FileHandle, IoStatusBlock, FileInformation, Length, FileInformationClass):
  #IN HANDLE FileHandle,
  #OUT PIO_STATUS_BLOCK IoStatusBlock,
  #OUT PVOID FileInformation,
  #IN ULONG Length,
  #IN FILE_INFORMATION_CLASS FileInformationClass
  return call_stdcall(211, "<IIIII", FileHandle, IoStatusBlock, FileInformation, Length, FileInformationClass)

def NtSetEvent(EventHandle, PreviousState):
  #IN HANDLE EventHandle,
  #OUT PLONG PreviousState OPTIONAL
  return call_stdcall(225, "<II", EventHandle, PreviousState)

def NtSetInformationFile(FileHandle, IoStatusBlock, FileInformation, Length, FileInformationClass):
  #IN HANDLE FileHandle,
  #OUT PIO_STATUS_BLOCK IoStatusBlock,
  #IN PVOID FileInformation,
  #IN ULONG Length,
  #IN FILE_INFORMATION_CLASS FileInformationClass
  return call_stdcall(226, "<IIIII", FileHandle, IoStatusBlock, FileInformation, Length, FileInformationClass)

def ObReferenceObjectByName(ObjectName, Attributes, ObjectType, ParseContext, Object):
  #IN POBJECT_STRING ObjectName,
  #IN ULONG Attributes,
  #IN POBJECT_TYPE ObjectType,
  #IN OUT PVOID ParseContext OPTIONAL,
  #OUT PVOID *Object
  return call_stdcall(247, "<IIIII", ObjectName, Attributes, ObjectType, ParseContext, Object)

def PsCreateSystemThreadEx(ThreadHandle, ThreadExtensionSize, KernelStackSize, TlsDataSize, ThreadId, StartRoutine, StartContext, CreateSuspended, DebuggerThread, SystemRoutine):
  #OUT PHANDLE ThreadHandle,
  #IN SIZE_T ThreadExtensionSize,
  #IN SIZE_T KernelStackSize,
  #IN SIZE_T TlsDataSize,
  #OUT PHANDLE ThreadId OPTIONAL,
  #IN PKSTART_ROUTINE StartRoutine,
  #IN PVOID StartContext,
  #IN BOOLEAN CreateSuspended,
  #IN BOOLEAN DebuggerThread,
  #IN PKSYSTEM_ROUTINE SystemRoutine OPTIONAL
  return call_stdcall(255, "<IIIIIIIIII", ThreadHandle, ThreadExtensionSize, KernelStackSize, TlsDataSize, ThreadId, StartRoutine, StartContext, CreateSuspended, DebuggerThread, SystemRoutine)

def RtlFillMemory(Destination, Length, Fill):
  #PVOID Destination,
  #ULONG Length,
  #UCHAR Fill
  call_stdcall(284, "<III", Destination, Length, Fill)

def RtlFillMemoryUlong(Destination, Length, Pattern):
  #PVOID Destination,
  #SIZE_T Length,
  #ULONG Pattern
  call_stdcall(285, "<III", Destination, Length, Pattern)

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

def XcSHAInit(pbSHAContext):
  #OUT PUCHAR pbSHAContext
  call_stdcall(335, "<I", pbSHAContext)

def XcSHAUpdate(pbSHAContext, pbInput, dwInputLength):
  #IN OUT PUCHAR pbSHAContext,
  #IN PUCHAR pbInput,
  #IN ULONG dwInputLength
  call_stdcall(336, "<III", pbSHAContext, pbInput, dwInputLength)

def XcSHAFinal(pbSHAContext, pbDigest):
  #IN PUCHAR pbSHAContext,
  #OUT PUCHAR pbDigest
  call_stdcall(337, "<II", pbSHAContext, pbDigest)


def XcHMAC(pbKey, dwKeyLength, pbInput, dwInputLength, pbInput2, dwInputLength2, pbDigest):
  #IN PUCHAR pbKey,
  #IN ULONG dwKeyLength,
  #IN PUCHAR pbInput,
  #IN ULONG dwInputLength,
  #IN PUCHAR pbInput2,
  #IN ULONG dwInputLength2,
  #OUT PUCHAR pbDigest
  call_stdcall(340, "<IIIIIII", pbKey, dwKeyLength, pbInput, dwInputLength, pbInput2, dwInputLength2, pbDigest)


def XcDESKeyParity(pbKey, dwKeyLength):
  #IN OUT PUCHAR pbKey,
  #IN ULONG dwKeyLength
  call_stdcall(346, "<II", pbKey, dwKeyLength)

def XcKeyTable(dwCipher, pbKeyTable, pbKey):
  #IN ULONG dwCipher,
  #OUT PUCHAR pbKeyTable,
  #IN PUCHAR pbKey
  call_stdcall(347, "<III", dwCipher, pbKeyTable, pbKey)

def XcBlockCryptCBC(dwCipher, dwInputLength, pbOutput, pbInput, pbKeyTable, dwOp, pbFeedback):
  #IN ULONG dwCipher,
  #IN ULONG dwInputLength,
  #OUT PUCHAR pbOutput,
  #IN PUCHAR pbInput,
  #IN PUCHAR pbKeyTable,
  #IN ULONG dwOp,
  #IN PUCHAR pbFeedback
  call_stdcall(349, "<IIIIIII", dwCipher, dwInputLength, pbOutput, pbInput, pbKeyTable, dwOp, pbFeedback)

def XboxLANKey():
  return pe.resolve_export(353)

def XboxAlternateSignatureKeys():
  return pe.resolve_export(354)

def XePublicKeyData():
  return pe.resolve_export(355)

def HalInitiateShutdown():
  call_stdcall(360, "")


def call_stdcall(function, types, *arguments):
  address = pe.resolve_export(function)
  registers = api.call(address, struct.pack(types, *arguments))
  return registers['eax']
