# This code is the hack for doing random read/writes using XBDM

Assembled using https://defuse.ca/online-x86-assembler.htm

```
# Disable memory protection
mov eax, cr0
push eax
and eax, 0xFFFEFFFF
mov cr0, eax

# Get arguments
mov edx, [esp+8]        # Get communication address
mov ebx, [edx+0]        # Get address
mov ecx, [edx+4]        # Get operation
mov eax, [edx+8]        # Data; Might need this for writes

do_read_u8: # 1
loop do_read_u16
mov al, [ebx]

do_read_u16: # 2
loop do_read_u32
mov ax, [ebx]

do_read_u32: # 3
loop do_write_u8
mov eax, [ebx]

do_write_u8: # 4
loop do_write_u16
mov [ebx], al

do_write_u16: # 5
loop do_write_u32
mov [ebx], ax

do_write_u32: # 6
loop do_call
mov [ebx], eax

do_call:
loop cleanup # 7
pusha # Backup all vars
mov [0x80010000], esp
# eax = how many bytes follow at [edx+12]
mov ecx, eax
sub esp, ecx
mov edi, esp
lea esi, [edx+12]
rep movsb
call ebx # Call function
mov esp, [0x80010000]
mov [esp + 7*4], eax # Replace eax on stack with new one
popa # Recover all vars and modified eax

cleanup:
mov [edx+8], eax        # Data; Might need this for reads
pop eax                 # Restore cr0 (memory protection)
mov cr0, eax
mov eax, 0x02DB0000     # Return Success (lower bits describe the response type)
ret 4
```

TODO:
As the stack still contains the actual buffer we could send all input data through the stack (with one network packet)
Likewise, the return data could be pushed directly into the return packet
