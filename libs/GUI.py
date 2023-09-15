import queue
import sys

import PySimpleGUI as sg
from PySimpleGUI import Element, Window

from libs.EventListener import EventListener
from libs.Logger import Logger

_default_layout = [
    [sg.Multiline(size=(80, 18), disabled=True, key='-OUTPUT-', autoscroll=True, expand_x=True,
                  expand_y=True)],
    [sg.Multiline(size=(80, 2), key='-INPUT-', enable_events=True, autoscroll=True,
                  do_not_clear=False, expand_x=True)]
]


class GUI(EventListener):
    __logger = Logger('GUI')  # 記錄器
    __output_queue = queue.Queue()  # 輸出暫存器
    __window: Window  # 主視窗
    __layout: list[list[Element]]  # 介面排版
    __title: str  # 應用程式標題
    __font: tuple[str, int]  # 字體
    __theme: str  # 主題

    def __init__(self, title,
                 font=('JetBrains Mono', 13),
                 theme='DarkBlue3',
                 layout=None):
        """
        初始化建構子

        :param title: 應用程式標題
        :type title: (str)
        :param layout: 介面排版
        :type layout: (list[list[Element]])
        :param font: 字體
        :type font: (tuple[str, int])
        :param theme: 主題
        :type theme: (str)
        """

        self.__layout = _default_layout if layout is None else layout
        self.__title = title
        self.__font = font
        self.__theme = theme

    def set_layout(self, layout):
        """
        設定介面排版

        :param layout:
        :type layout: (list[list[Element]])
        """

        self.__layout = layout

    def print(self, text):
        """
        向輸出暫存器添加文字

        :param text: 文字內容
        :type text: (str)
        """
        self.__output_queue.put(text)

    def println(self, text):
        """
        向輸出暫存器添加文字，並在句尾加上換行

        :param text: 文字內容
        :type text: (str)
        """
        self.print(text + '\n')

    async def build(self):
        """
        建構 GUI
        """

        sg.theme(self.__theme)
        try:
            self.__logger.info('正在初始化介面...')
            self.__window = sg.Window(self.__title, self.__layout, font=self.__font,
                                      return_keyboard_events=True, resizable=True, finalize=True)
            self.__logger.succ('介面初始化完成')
        except:
            self.__logger.err('介面初始化失敗')
            sys.exit(1)

        try:
            self.__logger.info('正在綁定事件監聽器...')
            self.__window['-INPUT-'].bind('<Return>', '_Enter')
            self.__logger.succ('事件監聽器綁定完成')
        except:
            self.__logger.err('事件監聽器綁定失敗')
            sys.exit(1)

        while True:
            # 事件名稱, 介面資料
            event, values = self.__window.read(timeout=100)

            # 若視窗被關閉
            if event == sg.WINDOW_CLOSED:
                self.__logger.info('正在關閉...')
                break  # 跳出迴圈

            # 如果使用者按下 Enter 鍵
            if event == '-INPUT-' + '_Enter':
                await self.__enter_event(values)

            # 嘗試取得並輸出暫存器內容
            try:
                self.__window['-OUTPUT-'].update(
                    self.__output_queue.get_nowait(), append=True)
            except queue.Empty:
                # 暫存器內容為空
                pass

        self.__window.close()

    ##################
    #  Private Func  #
    ##################
    async def __enter_event(self, values):
        # 將開頭與結尾的空格移除
        user_input = values['-INPUT-'].strip()

        # 若訊息為空, 則不理會事件
        if user_input == '':
            return

        # 呼叫輸入事件，可使用裝飾器接收
        await self.trigger('on_input_line', self, user_input)

        # 清空輸入框
        self.__window['-INPUT-'].update('')
