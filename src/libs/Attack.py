# import asyncio
# import threading
# import time
#
# from pymetasploit3.msfrpc import MsfRpcClient, ExploitModule, PostModule, EncoderModule, AuxiliaryModule, NopModule, \
#     PayloadModule, ShellSession, MeterpreterSession
#
# from libs.EventListener import EventListener
# from libs.Logger import Logger
# from libs.Payloads import Payloads
#
#
# class AttackError(Exception):
#     def __init__(self, msg):
#         self.msg = msg
#
#
# class Attack(EventListener):
#     __logger: Logger = Logger('ATK')
#     __rpc: MsfRpcClient
#     __rhost: str
#     __payload: Payloads
#     __module: ExploitModule | PostModule | EncoderModule | AuxiliaryModule | NopModule | PayloadModule
#     __options: dict[str, str] = {}
#     __session: MeterpreterSession | ShellSession
#     __read_thread: threading
#     __status: bool = False
#
#     def __init__(self, rpc, module, payload=Payloads.REVERSE_TCP, /,
#                  *args: tuple[str, str]):
#         """
#         初始化建構子
#
#         :param (MsfRpcClient) rpc:     執行客戶端
#         :param (Modules)      module:  攻擊模型
#         :param (Payloads)     payload: 執行負載
#         """
#
#         self.__rpc = rpc
#         self.__payload = payload
#
#         # 取得模型類型與名稱
#         first_slash_index = module.value.find('/')
#         mtype = module.value[:first_slash_index]
#         mname = module.value[first_slash_index + 1:]
#
#         # 初始化攻擊模型
#         self.__module = self.__rpc.modules.use(mtype, mname)
#
#         # 寫入 Options
#         for i in args:
#             if i[0] not in self.__module.options:
#                 self.__logger.warn(f'未知的參數: {i[0]}')
#             else:
#                 self.__module[i[0]] = i[1]
#
#     def setPayload(self, payload):
#         """
#         設定執行負載
#
#         :param (Payloads) payload: 執行負載
#         """
#
#         self.__payload = payload
#
#     def __check(self):
#         """
#         :raise AttackError: 當必要參數不完整
#         """
#
#         if len(self.__module.missing_required) > 1:
#             raise AttackError(f'必要參數不完整: {", ".join(self.__module.missing_required)}')
#
#     def run(self) -> str:
#         """
#         開始攻擊
#
#         :return: 訊息內容
#         :rtype:  (str)
#         """
#
#         # 檢查參數
#         self.__check()
#
#         # 回傳攻擊結果
#         response = self.__rpc.consoles.console(self.__rpc.consoles.console().cid) \
#             .run_module_with_output(self.__module, PayloadModule(self.__rpc, self.__payload.value))
#
#         # 開始讀取終端資料
#         if len(self.__rpc.sessions.list) != 0:
#             self.__session = \
#                 self.__rpc.sessions.session(
#                     list(self.__rpc.sessions.list.keys())[0]
#                 )
#             self.__status = True
#             self.__read_thread = threading.Thread(target=self.__read_thread)
#             self.__read_thread.start()
#
#         return response
#
#     def stop(self):
#         self.__status = False
#         self.__read_thread.join()
#         self.__session.stop()
#
#     ##################
#     #  Private Func  #
#     ##################
#     def __read_thread(self):
#         """
#         週期性線程
#         """
#
#
#         while self.__status:
#             time.sleep(0.1)
#
#             # 當程式關掉會爆炸，需要接錯誤
#             try:
#                 tmp = self.__session.read()
#                 if tmp != '':
#                     loop.run_until_complete(self.trigger('on_read', tmp))
#             except KeyError:
#                 pass
