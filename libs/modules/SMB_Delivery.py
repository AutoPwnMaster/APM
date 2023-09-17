from pymetasploit3.msfrpc import MsfRpcClient

from libs.Payloads import Payloads
from libs.modules.Basic import Basic


class SMB_Delivery(Basic):
    option_keys: list[str] = ['ContextInformationFile', 'DisablePayloadHandler', 'EXE::Custom', 'EXE::EICAR',
                              'EXE::FallBack', 'EXE::Inject', 'EXE::OldMethod', 'EXE::Path', 'EXE::Template',
                              'EnableContextEncoding', 'FILE_NAME', 'FOLDER_NAME', 'ListenerBindAddress',
                              'ListenerBindPort', 'ListenerComm', 'MSI::Custom', 'MSI::EICAR', 'MSI::Path',
                              'MSI::Template', 'MSI::UAC', 'Powershell::encode_final_payload',
                              'Powershell::encode_inner_payload', 'Powershell::exec_in_place', 'Powershell::exec_rc4',
                              'Powershell::method', 'Powershell::no_equals', 'Powershell::noninteractive',
                              'Powershell::persist', 'Powershell::prepend_protections_bypass',
                              'Powershell::prepend_sleep', 'Powershell::remove_comspec', 'Powershell::strip_comments',
                              'Powershell::strip_whitespace', 'Powershell::sub_funcs', 'Powershell::sub_vars',
                              'Powershell::wrap_double_quotes', 'SHARE', 'SMBDomain', 'SRVHOST', 'SRVPORT', 'VERBOSE',
                              'WORKSPACE']

    def __init__(self, rpc: MsfRpcClient, /, payload=Payloads.REVERSE_TCP, ContextInformationFile=None,
                 DisablePayloadHandler=None, EXE__Custom=None,
                 EXE__EICAR=None,
                 EXE__FallBack=None, EXE__Inject=None, EXE__OldMethod=None, EXE__Path=None, EXE__Template=None,
                 EnableContextEncoding=None, FILE_NAME=None, FOLDER_NAME=None, ListenerBindAddress=None,
                 ListenerBindPort=None, ListenerComm=None, MSI__Custom=None, MSI__EICAR=None, MSI__Path=None,
                 MSI__Template=None, MSI__UAC=None, Powershell__encode_final_payload=None,
                 Powershell__encode_inner_payload=None, Powershell__exec_in_place=None, Powershell__exec_rc4=None,
                 Powershell__method=None, Powershell__no_equals=None, Powershell__noninteractive=None,
                 Powershell__persist=None, Powershell__prepend_protections_bypass=None, Powershell__prepend_sleep=None,
                 Powershell__remove_comspec=None, Powershell__strip_comments=None, Powershell__strip_whitespace=None,
                 Powershell__sub_funcs=None, Powershell__sub_vars=None, Powershell__wrap_double_quotes=None, SHARE=None,
                 SMBDomain=None, SRVHOST=None, SRVPORT=None, VERBOSE=None, WORKSPACE=None
                 ):
        """

        :param rpc:
        :param payload:
        :param ContextInformationFile:
        :param DisablePayloadHandler:
        :param EXE__Custom:
        :param EXE__EICAR:
        :param EXE__FallBack:
        :param EXE__Inject:
        :param EXE__OldMethod:
        :param EXE__Path:
        :param EXE__Template:
        :param EnableContextEncoding:
        :param FILE_NAME:
        :param FOLDER_NAME:
        :param ListenerBindAddress:
        :param ListenerBindPort:
        :param ListenerComm:
        :param MSI__Custom:
        :param MSI__EICAR:
        :param MSI__Path:
        :param MSI__Template:
        :param MSI__UAC:
        :param Powershell__encode_final_payload:
        :param Powershell__encode_inner_payload:
        :param Powershell__exec_in_place:
        :param Powershell__exec_rc4:
        :param Powershell__method:
        :param Powershell__no_equals:
        :param Powershell__noninteractive:
        :param Powershell__persist:
        :param Powershell__prepend_protections_bypass:
        :param Powershell__prepend_sleep:
        :param Powershell__remove_comspec:
        :param Powershell__strip_comments:
        :param Powershell__strip_whitespace:
        :param Powershell__sub_funcs:
        :param Powershell__sub_vars:
        :param Powershell__wrap_double_quotes:
        :param SHARE:
        :param SMBDomain:
        :param SRVHOST:
        :param SRVPORT:
        :param VERBOSE:
        :param WORKSPACE:
        """
        super().__init__(rpc, 'windows/smb/smb_delivery', payload)

        for i in self.option_keys:
            if locals().get(i) is not None:
                self.set_option(i, locals().get(i))

    async def run(self):
        response = await super()._run()
        await self.trigger('on_read', response)

    def check_session(self):
        # TODO: 檢查連是否成功
        pass
