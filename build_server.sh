#!/bin/bash

set -e # 如果有錯誤則離開
if lsof -i :55553; then # 如果伺服器已經開啟
    echo "PORT 55553 has been turned on"
else
    echo "Building ... " 
    success=false # 預設為失敗
    msfrpcd -P $1 # 重頭戲 (開啟伺服器)
    for ((i = 0; i < 10; i += 1)); do # 嘗試 10 次檢測 PORT
        if lsof -i :55553; then
            success=true
            break
        fi
        sleep 1 # 等待 1 秒
    done
    
    if $success; then # 顯示成功與否
        echo "Building Successed !"
    else
        echo "Building Failed or Time out !"
    fi
fi