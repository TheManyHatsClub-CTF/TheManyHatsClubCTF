#!/usr/bin/python3

import requests

def main():
    url = 'http://192.168.254.137/flag'
    r1 = requests.post(url)
    print(r1.text)
    data = {"answer":str("{:.2f}".format(round(eval(r1.text.split('>')[2].split('<')[0]),2)))}
    r2 = requests.post(url,data=data,cookies=r1.cookies)
    print(r2.text)
    data = {"answer":str("{:.2f}".format(round(eval(r2.text.split('<')[1].split(':')[1]),2)))}
    r3 = requests.post(url,data=data,cookies=r2.cookies)
    print(r3.text)
    data = {"answer":str("{:.2f}".format(round(eval(r3.text.split('<')[1].split(':')[1]),2)))}
    r4 = requests.post(url,data=data,cookies=r3.cookies)
    print(r4.text)
    data = {"answer":str("{:.2f}".format(round(eval(r4.text.split('<')[1].split(':')[1]),2)))}
    r5 = requests.post(url,data=data,cookies=r4.cookies)
    print(r5.text)
    data = {"answer":str("{:.2f}".format(round(eval(r5.text.split('<')[1].split(':')[1]),2)))}
    r6 = requests.post(url,data=data,cookies=r5.cookies)
    print(r6.text)
    data = {"answer":str("{:.2f}".format(round(eval(r6.text.split('<')[1].split(':')[1]),2)))}
    r7 = requests.post(url,data=data,cookies=r6.cookies)
    print(r7.text)
    data = {"answer":str("{:.2f}".format(round(eval(r7.text.split('<')[1].split(':')[1]),2)))}
    r8 = requests.post(url,data=data,cookies=r7.cookies)
    print(r8.text)
    data = {"answer":str("{:.2f}".format(round(eval(r8.text.split('<')[1].split(':')[1]),2)))}
    r9 = requests.post(url,data=data,cookies=r8.cookies)
    print(r9.text)
    data = {"answer":str("{:.2f}".format(round(eval(r9.text.split('<')[1].split(':')[1]),2)))}
    r10 = requests.post(url,data=data,cookies=r9.cookies)
    print(r10.text)
    data = {"answer":"YES_I_CAN!"}
    r11 = requests.post(url,data=data,cookies=r10.cookies)
    print(r11.text)

if __name__ == "__main__":
    main()
