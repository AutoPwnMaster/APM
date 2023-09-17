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
    __command_history: list[str] = []  # 指令輸入紀錄
    __current_pos: int = 0  # 目前指令輸入紀錄位置 (0)
    __latest_content: str

    def __init__(self, title,
                 font=('JetBrains Mono', 13),
                 theme='DarkBlue3',
                 layout=None):
        """
        初始化建構子

        :param (str)                 title:  應用程式標題
        :param (list[list[Element]]) layout: 介面排版
        :param (tuple[str, int])     font:   字體
        :param (str)                 theme:  主題
        """

        self.__layout = _default_layout if layout is None else layout
        self.__title = title
        self.__font = font
        self.__theme = theme

    def set_layout(self, layout):
        """
        設定介面排版

        :param (list[list[Element]]) layout: 介面
        """

        self.__layout = layout

    def print(self, text):
        """
        向輸出暫存器添加文字

        :param (str) text: 文字內容
        """

        self.__output_queue.put(text)

    def println(self, text):
        """
        向輸出暫存器添加文字，並在句尾加上換行

        :param (str) text: 文字內容
        """

        self.print(text + '\n')

    def build(self):
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
            self.__window['-INPUT-'].bind('<Up>', '_Up')
            self.__window['-INPUT-'].bind('<Down>', '_Down')
            self.__logger.succ('事件監聽器綁定完成')
        except:
            self.__logger.err('事件監聽器綁定失敗')
            sys.exit(1)

        # 主迴圈
        while True:
            # 事件名稱, 介面資料
            event, values = self.__window.read(timeout=100)

            # 若視窗被關閉
            if event == sg.WINDOW_CLOSED:
                self.__logger.info('正在關閉...')
                break  # 跳出迴圈

            match event:
                case '-INPUT-_Enter':
                    self.__enter_event(values['-INPUT-'].strip())

                case '-INPUT-_Up':
                    self.__up_event(values['-INPUT-'].strip())

                case '-INPUT-_Down':
                    self.__down_event()

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
    def __enter_event(self, input):
        # 若訊息為空, 則不理會事件
        if input == '':
            return

        # 記錄指令
        self.__command_history.append(input)
        self.__current_pos = 0

        # 呼叫輸入事件，可使用裝飾器接收
        self.trigger('on_input_line', self, input)

        # 清空輸入框
        self.__window['-INPUT-'].update('')

    def __up_event(self, text):
        # 無更多紀錄
        if self.__current_pos == len(self.__command_history):
            return

        if self.__current_pos == 0:
            self.__latest_content = text

        self.__current_pos += 1

        # 更新輸入框
        self.__window['-INPUT-'].update(
            self.__command_history[-self.__current_pos]
        )

    def __down_event(self):
        # 已經是最新了
        if self.__current_pos == 0:
            return

        # 更新輸入框
        if self.__current_pos == 1:
            self.__current_pos = 0
            self.__window['-INPUT-'].update(self.__latest_content)
        else:
            self.__window['-INPUT-'].update(
                self.__command_history[-self.__current_pos + 1]
            )
            self.__current_pos -= 1
