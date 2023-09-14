import os
from datetime import datetime

if __name__ == '__main__':
    os.system("")


class Style:
    RESET = '\33[0m'
    GREY = '\x1b[38;2;120;120;120m'
    INFO = '\x1b[1;37;44m'
    SUCC = '\x1b[1;30;42m'
    WARN = '\x1b[1;30;43m'
    ERROR = '\x1b[1;37;41m'


class Logger:
    __prefix: str

    def __init__(self, prefix='LOG'):
        """
        輸出日誌

        :param  prefix:      前綴
        :type   prefix:      (str)
        """

        self.__prefix = prefix
        self.succ('初始化完成')

    def info(self, message):
        """
        向終端輸出「記錄」訊息

        :param   message: 文字
        :type    message: (str)
        """

        print(f'{Style.GREY}{self.time()}{Style.RESET} '
              f'{Style.INFO}INFO{Style.RESET} => '
              f'[{self.__prefix}] '
              f'{message}'
              f'{Style.RESET}')

    def succ(self, message):
        """
        向終端輸出「成功」訊息

        :param   message: 文字
        :type    message: (str)
        """

        print(f'{Style.GREY}{self.time()} '
              f'{Style.SUCC}SUCC{Style.RESET} => '
              f'[{self.__prefix}] '
              f'{message}'
              f'{Style.RESET}')

    def warn(self, message):
        """
        向終端輸出「警告」訊息

        :param   message: 文字
        :type    message: (str)
        """

        print(f'{Style.GREY}{self.time()} '
              f'{Style.WARN}WARN{Style.RESET} => '
              f'[{self.__prefix}] '
              f'{message}'
              f'{Style.RESET}')

    def err(self, message):
        """
        向終端輸出「錯誤」訊息

        :param   message: 文字
        :type    message: (str)
        """

        print(f'{Style.GREY}{self.time()} '
              f'{Style.ERROR}ERR!{Style.RESET} => '
              f'[{self.__prefix}] '
              f'{message}'
              f'{Style.RESET}')

    @staticmethod
    def time():
        """
        取得當前時間(毫秒取三位)
        e.g. 02:47:48.254

        :return: 時間 '%H:%M:%S.%f'
        :rtype:  (str)
        """

        return datetime.now().strftime('%H:%M:%S.%f')[:-3]

# if __name__ == '__main__':
#     logger = Logger('tmp')
#     logger.info('HI')
#     logger.succ('HI')
#     logger.warn('HI')
#     logger.err('HI')
