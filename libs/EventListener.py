"""
事件監聽器模式說明

事件監聽器模式允許開發者在未來的開發中更容易擴展和維護程式碼。
此模式允許使用者透過「裝飾器」向「指定班級」添加學生（即事件的行為）。

班級(Event) <-> 學校(EventListener) 之間的關係說明:

Event:
    - 表示一個班級，每個班級只有一個名字（例如資三甲）。
    - 班級內可以有多個學生，每個學生都有他們特定會做的事情。
    - 這裡的重點不在於誰是學生，而在於他們的行為。

    add_listener:    將學生的行為添加到此班級。
    remove_listener: 從此班級中移除學生的行為。
    trigger:         觸發器。異步執行此班級中所有學生的行為。

----------------------------------------------------------------

EventListener:
    - 表示學校，學校內有多個班級。
    - 學校可以透過觸發器廣播班級名稱，使班級中的所有學生都能異步執行他們的行為。

    event:   裝飾器。根據函數名稱，將函數行為添加到對應的班級中。
    trigger: 觸發器。根據班級名稱，異步執行該班級中所有學生的行為。
"""


class Event:
    def __init__(self):
        self.__listeners = []

    # 添加被觸發器
    def add_listener(self, func):
        if func not in self.__listeners:
            self.__listeners.append(func)

    # 移除被觸發器
    def remove_listener(self, func):
        if func in self.__listeners:
            self.__listeners.remove(func)

    # 觸發觸發器
    async def trigger(self, *args, **kwargs):
        for listener in self.__listeners:
            await listener(*args, **kwargs)


class EventListener:
    __events: dict[str, Event] = {}

    def event(self, func):
        """
        裝飾器。將會根據事件與函數名稱異步觸發。
        可以重複定義多個函數，無法保證執行先後順序。

        :param   (function) func: 觸發函數
        :return:                  觸發函數
        :rtype:  (function)
        """

        self.__events \
            .setdefault(func.__name__, Event()) \
            .add_listener(func)

        return func

    async def trigger(self, event_name, *args, **kwargs):
        """
        觸發事件監聽器。

        :param (str) event_name: 事件名稱。通常是裝飾器函數名稱
        :param       args:       元組參數。接收任意數量的位置引數
        :param       kwargs:     字典參數。接收任意數量的關鍵字引數
        """

        if event_name in self.__events:
            await self.__events[event_name].trigger(*args, **kwargs)
