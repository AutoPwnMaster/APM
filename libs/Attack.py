from pymetasploit3.msfrpc import MsfRpcClient, ExploitModule, PostModule, EncoderModule, AuxiliaryModule, NopModule, \
    PayloadModule

from libs.Modules import Modules
from libs.Payloads import Payloads


class Attack:
    __rpc: MsfRpcClient
    __rhost: str
    __module_path: Modules
    __payload: Payloads
    __module: ExploitModule | PostModule | EncoderModule | AuxiliaryModule | NopModule | PayloadModule

    def __init__(self, rpc, rhost, module, payload):
        """
        初始化建構子

        :param rpc:     執行客戶端
        :type rpc:      (MsfRpcClient)
        :param rhost:   目標主機IP
        :type rhost:    (str)
        :param module:  攻擊模型
        :type module:   (Modules)
        :param payload: 執行負載
        :type payload:  (Payloads)
        """

        self.__rpc = rpc
        self.__rhost = rhost
        self.__module_path = module
        self.__payload = payload

    def setModule(self, module):
        """
        設定攻擊模型

        :param module:
        :type module: Modules
        """

        self.__module_path = module

    def setPayload(self, payload):
        """
        設定執行負載

        :param payload: 執行負載
        :type payload: Payloads
        """

        self.__payload = payload

    def run(self) -> str:
        """
        開始攻擊

        :return:
        :rtype: (str)
        """

        # 取得模型類型與名稱
        first_slash_index = self.__module_path.value.find('/')
        mtype = self.__module_path.value[:first_slash_index]
        mname = self.__module_path.value[first_slash_index + 1:]

        # 初始化攻擊模型
        self.__module = self.__rpc.modules.use(mtype, mname)

        # 設定攻擊目標
        self.__module['RHOSTS'] = self.__rhost

        # 回傳攻擊結果
        return self.__rpc.consoles.console(self.__rpc.consoles.console().cid) \
            .run_module_with_output(self.__module, PayloadModule(self.__rpc, self.__payload.value))
