class Modules(str):
    # excellent
    SMB_DELIVERY = 'windows/smb/smb_delivery'
    MS10_061_SPOOLSS = 'windows/smb/ms10_061_spoolss'
    MS10_046_SHORTCUT_ICON_DLLLOADER = 'windows/smb/ms10_046_shortcut_icon_dllloader'
    SMB_RELAY = 'windows/smb/smb_relay'
    MS15_020_SHORTCUT_ICON_DLLLOADER = 'windows/smb/ms15_020_shortcut_icon_dllloader'

    # great
    TIMBUKTU_PLUGHNTCOMMAND_BOF = 'windows/smb/timbuktu_plughntcommand_bof'
    SMB_DOUBLEPULSAR_RCE = 'windows/smb/smb_doublepulsar_rce'
    NETIDENTITY_XTIERRPCPIPE = 'windows/smb/netidentity_xtierrpcpipe'
    MS08_067_NETAPI = 'windows/smb/ms08_067_netapi'

    # good
    MS06_066_NWAPI = 'windows/smb/ms06_066_nwapi'
    MS03_049_NETAPI = 'windows/smb/ms03_049_netapi'
    MS06_025_RASMAN_REG = 'windows/smb/ms06_025_rasmans_reg'
    MS04_011_LSASS = 'windows/smb/ms04_011_lsass'
    MS06_040_NETAPI = 'windows/smb/ms06_040_netapi'
    MS09_050_SMB2_NEGOTIATE_FUNC_INDEX = 'windows/smb/ms09_050_smb2_negotiate_func_index'
    MS04_031_NETDDE = 'windows/smb/ms04_031_netdde'
    MS05_039_PNP = 'windows/smb/ms05_039_pnp'
    MS06_066_NWWKS = 'windows/smb/ms06_066_nwwks'

    # normal
    MS17_010_PSEXE = 'windows/smb/ms17_010_psexec'

    # average
    SMB_RRAS_ERRATICGOPHER = 'windows/smb/smb_rras_erraticgopher'
    MS17_010_ETERNALBLUE = 'windows/smb/ms17_010_eternalblue'
    MS06_025_RRAS = 'windows/smb/ms06_025_rras'
    CVE_2020_0796_SMBGHOST = 'windows/smb/cve_2020_0796_smbghost'

    # low
    MS04_007_KILLBILL = 'windows/smb/ms04_007_killbill'

    # manual
    PSEXE = 'windows/smb/psexec'
    MS06_070_WKSSVC = 'windows/smb/ms06_070_wkssvc'
    SMB_SHADOW = 'windows/smb/smb_shadow'
    WEBEXEC = 'windows/smb/webexec'
    GROUP_POLICY_STARTUP = 'windows/smb/group_policy_startup'
    GENERIC_SMB_DLL_INJECTION = 'windows/smb/generic_smb_dll_injection'
    MS07_029_MSDNS_ZONENAME = 'windows/smb/ms07_029_msdns_zonename'