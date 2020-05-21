The code is based on other code sources and kinda messed up, but works like charm.

First of all based on the project below i used the IR data to hex code translator.
https://github.com/Lime-Parallelogram/IR-Code-Decoder--

I had to modify his method because it was eating the CPU constantly, now it doesnt use much cpu.
kodi-send had a problem with too many commands, i fixed the problem with the socket solution.
I dont understand sockets yet, but it worked out.

I will upgrade the code and make it more readable if i will have time.


To make it work just download the files and run the CLI file from the IR-Code_Decoder project. 
Change the ip, pin, button codes and names in the remote file and run it.
