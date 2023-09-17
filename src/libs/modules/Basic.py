import asyncio
import threading
import time

from pymetasploit3.msfrpc import PayloadModule, ExploitModule, MsfRpcClient, MeterpreterSession

from src.libs.EventListener import EventListener
from src.libs.Logger import Logger


class Basic(EventListener):
    # Class Setting
    _logger: Logger

    # Module Setting
    __module: ExploitModule
    __payload: PayloadModule
    __rpc: MsfRpcClient

    # Session Setting
    __session_id: '-1'
    __session: MeterpreterSession = None
    __status: bool = False
    __read_thread: threading

    def __init__(self, rpc: MsfRpcClient, module_name: str, payload_name: str):
        self.__rpc = rpc
        self.__module = rpc.modules.use('exploit', module_name)
        self._logger = Logger(module_name[module_name.rfind('/') + 1:])
        self.__payload = rpc.modules.use('payload', payload_name)
        self.__read_thread = threading.Thread(target=self.__read)

    def set_module_option(self, key, value):
        """
        設定 Module 參數

        :param (str) key:   鍵
        :param (str) value: 值
        """

        self.__module[key] = value

    def set_payload_option(self, key, value):
        """
        設定 Payload 參數

        :param (str) key:   鍵
        :param (str) value: 值
        """

        self.__payload[key] = value

    # Must be async
    async def _run(self) -> str:
        """
        開始攻擊

        :return: 訊息內容
        :rtype:  (str)
        """

        self._logger.info('正在攻擊...')

        # 使用 run_in_executor 來非阻塞地執行 RPC 請求
        # response = self.__rpc.consoles \
        #     .console(self.__rpc.consoles.console().cid) \
        #     .run_module_with_output(self.__module, PayloadModule(self.__rpc, self.__payload))

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            self.__rpc.consoles.console(self.__rpc.consoles.console().cid).run_module_with_output,
            self.__module, self.__payload
        )

        self._logger.info('攻擊結束')
        return response

    def set_session(self, session_id):
        """

        :param (str) session_id:
        :return:
        """
        self.__session_id = session_id

        if session_id != '-1':
            self.__session = self.__rpc.sessions.session(session_id)
            """
            可使用 @self.event 裝飾器，並搭配 def on_read(): 函數做使用，實做出事件監聽器效果
            """

            if self.__session_id == '-1':
                self._logger.warn('cannot start read, cause session is empty!')
                return

            self.__status = True
            self.__read_thread.start()

    def stop(self):
        self._logger.info('正在關閉...')
        self.__status = False
        if self.__read_thread.is_alive():
            self.__read_thread.join()
        if self.__session is not None:
            self.__session.stop()
        self._logger.succ('關閉完成')

    ##################
    #  Private Func  #
    ##################
    def __read(self):
        """
        週期性協程
        """

        self._logger.info(f'開始監聽 session: {self.__session_id}')
        self.trigger('on_session_created', self.__session_id)
        while self.__status:
            time.sleep(0.1)

            try:
                tmp = self.__session.read()
                if tmp != '':
                    self.trigger('on_read', tmp)
            except KeyError:
                pass
