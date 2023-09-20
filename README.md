### Features

- 使用 [Pymetasploit3](https://github.com/DanMcInerney/pymetasploit3) 庫自動化攻擊
- 友善 GUI 介面
- 已復現：
  - [MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption](https://www.rapid7.com/db/modules/exploit/windows/smb/ms17_010_eternalblue/)
  - [SMB Delivery](https://www.rapid7.com/db/modules/exploit/windows/smb/smb_delivery/)
  - [SMB Login](https://www.rapid7.com/db/modules/auxiliary/scanner/smb/smb_login/)

# Auto Pwn Master

![](https://media.discordapp.net/attachments/1032292845853360232/1154036158016270476/pngwing.com.png?width=300&height=335)


## Description

0. 執行 `msfrpcd -P salt` 建立位於連接埠 **55553** 的服務
0. 再編輯 `src/Main.py` 內的攻擊方法與參數，如 IPv4，連接埠等
0. 最後執行 `src/Main.py` 開始攻擊

---

幾乎所有功能與方法都已包裝成「class」與「def」
可以從 `/srv/lib` 開始查看

---

非 `/src/\*` 的檔案均為測試用途，運行不保證其成功與穩定性
