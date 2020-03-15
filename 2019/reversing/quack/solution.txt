Name: quack
Description: Find the flag!
Flag: TMHC{d0nt_p1ug_m3_1n}

Solution: It's a avr elf executable, compiled for the malduino bad usb (duckyusb), which is essentially an atmega32u4 board.
Running strings on the file will reveal the text "Here is your flag:" but the actual flag isn't showing up in the binary.
the tool avr-objdump can be used to disassemble the executable: avr-objdump -d quack.elf
A lot of the code is irrelevant, we just need to follow the main function. There are a lot of pieces that look like the following

    176c:	64 e0       	ldi	r22, 0x04	; 4
    176e:	70 e0       	ldi	r23, 0x00	; 0
    1770:	80 e0       	ldi	r24, 0x00	; 0
    1772:	90 e0       	ldi	r25, 0x00	; 0
    1774:	0e 94 37 04 	call	0x86e	; 0x86e <delay>
    1778:	83 eb       	ldi	r24, 0xB3	; 179
    177a:	90 e0       	ldi	r25, 0x00	; 0
    177c:	0e 94 b2 06 	call	0xd64	; 0xd64 <_Z7typeKeyi>
    1780:	83 eb       	ldi	r24, 0xB3	; 179
    1782:	90 e0       	ldi	r25, 0x00	; 0
    1784:	0e 94 b2 06 	call	0xd64	; 0xd64 <_Z7typeKeyi>
    1788:	83 eb       	ldi	r24, 0xB3	; 179
    178a:	90 e0       	ldi	r25, 0x00	; 0


function calls to <delay> and some kind of typekey function <_Z7typeKeyi>
the important argument for <delay> seems to be in r22 (0x04)
the important argument for <_Z7typeKeyi> seems to be in r24 (0xB3)

it checks out because the default delay before a key pressed is 4
(not after a repeated key press)

in the example the TAB key is pressed 3 times
the key values can be found here: https://www.arduino.cc/en/Reference/KeyboardModifiers
    KEY_TAB 	0xB3 	179 

Another function call is <_ZN5Print5writeEPKhj> which types a static string
it looks like this:

    1730:	4b e0       	ldi	r20, 0x0B	; 11
    1732:	50 e0       	ldi	r21, 0x00	; 0
    1734:	6e e3       	ldi	r22, 0x3E	; 62
    1736:	71 e0       	ldi	r23, 0x01	; 1
    1738:	83 e0       	ldi	r24, 0x03	; 3
    173a:	92 e0       	ldi	r25, 0x02	; 2
    173c:	0e 94 c0 02 	call	0x580	; 0x580 <_ZN5Print5writeEPKhj>

the two important arguments for this function are in r20 and r22 (length and .data offset)
By looking at the .data section with the command "avr-objdump quack.elf -j .data -d" we can see some strings at the bottom

00800132 <_ZTV9Keyboard_>:
  800132:	00 00 00 00 c5 06 c0 02 dc 06 db 06 63 68 61 72     ............char
  800142:	6d 61 70 2e 65 78 65 00 48 65 72 65 20 69 73 20     map.exe.Here is 
  800152:	79 6f 75 72 20 66 6c 61 67 3a 00 00                 your flag:..

so 0x3E (62 dec) is our offset in the example and we see that 0x142-0x4 = 0x3E
0x0B (11 dec) bytes from the offset 0x3E gives us the string "charmap.exe"
Now we know how that function call operates

From here all keypresses can be documented and reproduced, either manually or by re-creating the duckyscript or what else

Short explanation of the program: 
	1. presses GUI+R and types charmap.exe
	2. types out "Here is your flag:"
	3. uses tab, arrow keys & enter to produce the actual flag

Disclaimer: It might be possible to actually flash and run the executable yourself and see the program in action
This solution is also legitimate, but the player requires the exact same hardware as i don't think it can be emulated/simulated
I have not actually tested in that direction.
