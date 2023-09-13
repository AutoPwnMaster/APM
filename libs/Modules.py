from enum import Enum


class Modules(str, Enum):
    # excellent
    SMB_DELIVERY = 'exploit/windows/smb/smb_delivery'
    IPASS_PIPE_EXEC = 'exploit/windows/smb/ipass_pipe_exec'
    MS10_061_SPOOLSS = 'exploit/windows/smb/ms10_061_spoolss'
    MS10_046_SHORTCUT_ICON_DLLLOADER = 'exploit/windows/smb/ms10_046_shortcut_icon_dllloader'
    SMB_RELAY = 'exploit/windows/smb/smb_relay'
    MS15_020_SHORTCUT_ICON_DLLLOADER = 'exploit/windows/smb/ms15_020_shortcut_icon_dllloader'

    # great
    TIMBUKTU_PLUGHNTCOMMAND_BOF = 'exploit/windows/smb/timbuktu_plughntcommand_bof'
    SMB_DOUBLEPULSAR_RCE = 'exploit/windows/smb/smb_doublepulsar_rce'
    NETIDENTITY_XTIERRPCPIPE = 'exploit/windows/smb/netidentity_xtierrpcpipe'
    MS08_067_NETAPI = 'exploit/windows/smb/ms08_067_netapi'

    # good
    MS06_066_NWAPI = 'exploit/windows/smb/ms06_066_nwapi'
    MS03_049_NETAPI = 'exploit/windows/smb/ms03_049_netapi'
    MS06_025_RASMAN_REG = 'exploit/windows/smb/ms06_025_rasmans_reg'
    MS04_011_LSASS = 'exploit/windows/smb/ms04_011_lsass'
    MS06_040_NETAPI = 'exploit/windows/smb/ms06_040_netapi'
    MS09_050_SMB2_NEGOTIATE_FUNC_INDEX = 'exploit/windows/smb/ms09_050_smb2_negotiate_func_index'
    MS04_031_NETDDE = 'exploit/windows/smb/ms04_031_netdde'
    MS05_039_PNP = 'exploit/windows/smb/ms05_039_pnp'
    MS06_066_NWWKS = 'exploit/windows/smb/ms06_066_nwwks'

    # normal
    MS17_010_PSEXE = 'exploit/windows/smb/ms17_010_psexec'

    # average
    SMB_RRAS_ERRATICGOPHER = 'exploit/windows/smb/smb_rras_erraticgopher'
    MS17_010_ETERNALBLUE = 'exploit/windows/smb/ms17_010_eternalblue'
    MS06_025_RRAS = 'exploit/windows/smb/ms06_025_rras'
    CVE_2020_0796_SMBGHOST = 'exploit/windows/smb/cve_2020_0796_smbghost'

    # low
    MS04_007_KILLBILL = 'exploit/windows/smb/ms04_007_killbill'

    # manual
    PSEXE = 'exploit/windows/smb/psexec'
    MS06_070_WKSSVC = 'exploit/windows/smb/ms06_070_wkssvc'
    SMB_SHADOW = 'exploit/windows/smb/smb_shadow'
    WEBEXEC = 'exploit/windows/smb/webexec'
    GROUP_POLICY_STARTUP = 'exploit/windows/smb/group_policy_startup'
    GENERIC_SMB_DLL_INJECTION = 'exploit/windows/smb/generic_smb_dll_injection'
    MS07_029_MSDNS_ZONENAME = 'exploit/windows/smb/ms07_029_msdns_zonename'
