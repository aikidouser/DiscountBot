# 特價通知機器人

<font style="color:red;font-size:30px"> 這個機器人因存在重大錯誤，已暫停運行</font>

1. 查詢商品的價格
2. 使用此機器人將商品頁面加入清單
3. 會定期查詢價格，若低於原本的價格將會通知使用者

# 使用手冊

## 新增追蹤商品

### 目前只支援

- 24hpchome
  - 網址內需包含 24h, pchome, prod，其需皆可無視
  - 範例
    - <https://24h.pchome.com.tw/prod/DCAYKO-A90090S6A>
    - ![](https://i.imgur.com/CWgy8oA.png)
- momo
  - 網址內需包含 momoshop, goods, i_code，其餘皆可無視
  - 範例
    - <https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=5681462>
    - ![](https://i.imgur.com/pvgVjjR.png)

### 使用方式

- 單純貼上商品網址

- 電腦
  - 直接發送即可
- 手機
  - 推薦：分享頁面到聊天室
  - 可複製貼上

### 回應

- 成功
- 已經在列表裡
- 失敗
  - 請一段時間後重新嘗試

## 刪除追蹤商品

### 使用方式

### 回應

## 列出追蹤商品

### 使用方式

- 直接輸人 /list

### 回應

- pchome 與 momo 分兩則訊息列出

## 教學

- 直接輸入 /help
- 仔細看這篇

## 特價通知

- 順利找到現在的新價格

  - 如果

    - 比原本便宜 :arrow_right: 發訊息通知

    - 比原本貴 :arrow_right: 無視

      > 從特價變回原價（較貴的價格）

- 查新價格的時候出了一點意外
  - 發訊息和連結通知

# 程式架構

## 處理商品追蹤清單

### bot_main.py

- python-telegram-bot 的基本設定
  - 指令
  - workers 的數目：同時有多少執行緒處理指令。最大100。

### MsgReplyer.py

- 針對傳來的指令給出回覆
  - start_cmd
    - 剛加入機器人時的回傳訊息
  - help_cmd
    - 相關教學
  - add_cmd
  - del_cmd
  - list_cmd
  - exp_msg
  - error_callback

### CmdReplyer.py

### ECommHandler.py

## 更新商品價格

### notf_main.py

### Notification.py
