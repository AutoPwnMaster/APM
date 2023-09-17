import asyncio

from pymetasploit3.msfrpc import PayloadModule, ExploitModule, MsfRpcClient, MeterpreterSession, ShellSession

from libs.EventListener import EventListener
from libs.Logger import Logger


class Basic(EventListener):
    # Class Setting
    _logger: Logger

    # Module Setting
    __module: ExploitModule
    __payload: PayloadModule
    __rpc: MsfRpcClient

    # Session Setting
    __session_id: '-1'
    __session: MeterpreterSession | ShellSession = None
    __status: bool = False
    __loop: asyncio.events = asyncio.new_event_loop()

    def __init__(self, rpc: MsfRpcClient, module_name: str, payload_name: str):
        self.__rpc = rpc
        self.__module = rpc.modules.use('exploit', module_name)
        self._logger = Logger(module_name[module_name.rfind('/') + 1:])
        self.__payload = rpc.modules.use('payload', payload_name)

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
        print(self.__rpc.sessions.list)
        if session_id != '-1':
            self.__session = self.__rpc.sessions.session(session_id)

    def start_read(self):
        """
        將異步執行 :meth:`__read_thread` 函數。
        可使用 @self.event 裝飾器，並搭配 async def on_read(): 函數做使用，實做出事件監聽器效果
        """

        if self.__session_id == '-1':
            self._logger.warn('cannot start read, cause session is empty!')
            return

        self._logger.info(f'開始監聽 session: {self.__session_id}')

        print(type(self.__session))  # TODO: check type and fix it

        self.__status = True
        asyncio.set_event_loop(self.__loop)
        self.__loop.create_task(self.__read_coroutine())

    def stop(self):
        self._logger.info('正在關閉...')
        self.__status = False
        self.__loop.stop()
        self.__loop.close()
        if self.__session is not None:
            self.__session.stop()
        self._logger.succ('關閉完成')

    ##################
    #  Private Func  #
    ##################
    async def __read_coroutine(self):
        """
        週期性協程
        """
        while self.__status:
            # 使用 asyncio 版本的 sleep
            await asyncio.sleep(0.1)

            try:
                tmp = self.__session.read()
                if tmp != '':
                    await self.trigger('on_read', tmp)
            except KeyError:
                pass
