Title:
Lotto-Win

Description:
Lotto-Win is a new Lottery Platform that is open source. Use their vulnerabilities to end up being rich!

Difficulty:
Easy - Medium

Flag:
TMHC{Lucki3r_th4n_Pelayo}






How to set up the server
------------------------

lottery.py is the python file that contains the code for the CTF. It should be set up in the server with the command:
nc -lvp 10893 -e ./lottery.py

The users must connect to the CTF hosted in the server using the command:
nc ip.ip.ip.ip 10893