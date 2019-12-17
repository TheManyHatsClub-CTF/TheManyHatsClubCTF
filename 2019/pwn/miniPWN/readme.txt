Name: miniPwn
Description: Always use protections
Flag: TMHC{h4v3_y0u_h34rd_0f_SROP}

Solution: The vulnerability is a simple BOF but cannot be exploited with the usual methods. ASLR and NX are both enabled, ASLR can be circumvented by leaking a memory address. Though this doesn't help because the stack is non-executable, so you can't jump to your own shellcode. Neither is classic ROP possible because there aren't enough gadgets to perform code execution. You can't perform an execve syscall because you can't control the rdi register.
Another possible exploit technique: SROP (Sigreturn Oriented Programming)

Exploit Chain Explanation:

- return to read call and read 0xf bytes (sigret syscall)
  successful read syscall will set eax to the number of read bytes
  that way we can control the value in eax from 0 to 300 (read_size)
- return to syscall_ret gadget, eax = 0xf -> sigret syscall will be made
  through sigreturn we can control all registers
- set up registers for a memset call
  eax = 0xa -> memset syscall
  rdi = 0x400000 -> memory that we will adjust
  rsi = 0x1000 -> size
  rdx = 0x7 -> mode (rwx)
  rsp = 0x400018 -> points to entry point of the program
  rip = syscall_ret -> set instruction pointer to the syscall;ret gadget
- because we set rsp to the entry point, the program will rerun after the memset call
  but with the stack at the address 0x400000 and rwx permissions
- trigger the overflow again, write some shellcode and jump to it (we know the stack address)