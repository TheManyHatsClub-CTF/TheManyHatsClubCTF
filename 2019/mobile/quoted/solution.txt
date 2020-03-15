Name: quoted
Description:
Files: quoted.apk
Flag: TMHC{PAY_ATTENTION_IN_CLASS}

It's a simple Android app that's supposed to print random quotes (offline & 
api mode) and lets you copy them to the clipboard.
the goal is to simply reverse engineer it and find the flag, which is given in
the correct format.

First you need to find the correct password because some parts of the app are
encrypted via AES and cannot be accessed in any other way. Once you extracted
strings.xml (e.g. apktool) there are a few interesting values to be found.
Obvious ones would be "secret", "flag", "username" & "password". The "secret"
is an encrypted and base64 encoded string, which isn't important to solve the
challenge. The "flag" value is the string "Just no" base64 encoded, useless.
The "username" value is plaintext and is actually the required username. The
"password" value is an obfuscated version of the real password and can be
deobfuscated with jetty-util:
https://mvnrepository.com/artifact/org.eclipse.jetty/jetty-util/9.4.24.v20191120
With the obtained credentials it's possible to login and use the App and
possibly decrypt encrypted parts of the app. To get the flag we must call the
printFlag() method from the FlagPrinter class (names might be obfuscated).
The unencrypted class FlagPrinter has a method like that but it actually
just prints an empty string. On a closer look at MainActivity you will notice
that the onLongClick (i.e. the copy-to-clipboard) method tries to load a
class, create an instance of it and invoke a method called "printFlag".
On fail it calls the empty printFlag() method. the loadClass() method takes
the data string from strings.xml, base64decodes it, decrypts it and finally
loads it to memory via a InMemoryDexClassLoader. If you managed to find
the correct credentials, then it should invoke the correct "printFlag" method
once the onLongClick method is called. Now something should get printed to
System.out. Instead of the flag, "Try Harder" will be printed. By observing
memory or decompiling our decrypted new .dex you will see that this
FlagPrinter class has another method called victory(), which will print the
obfuscated flag. jetty-util can be used again to deobfuscate it and receive
the final flag!
