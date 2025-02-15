# Discord AI聊天機器人
**注意！因為跟原本的儲存庫有點差異，請一定要讀這篇！**
# 前言
這是**我從高一開始製作的AI Discord聊天機器人**  
為了做學習歷程所以將程式碼整理整理，順便處理了配置的東西，讓大家更好使用

關於**原本的儲存庫**，因為code有點屎所以**被我關成私人了**，不過如果有重大更新我也會把這裡更新一遍所以不用太擔心

看在我這麼認真的份上幫我按顆星星吧 :D
# 簡介
這是一個使用**Discord.py**與**Gemini API**開發的Discord bot    
* 功能
    * 在一般頻道mention你的機器人或者reply機器人的任意訊息，即可與AI對話
    * 可以讀取訊息中附帶的**圖片**
    * 支援語音功能，可與使用者**在語音頻道中對話**
    * 查詢**天氣**
    * 查詢**當日股價**、**公司營收資訊**(需提供AI欲查公司之股票代碼)
    * 訊息中**給予連結**可以**讀取網頁**
    * 在`settings/system_prompt`中可以寫系統提示詞，自訂你的AI
# 配置
## 安裝必要Python庫
請在終端執行：
```bash
pip install -r requirements.txt
```
## FFmpeg
由於語音功能需要`FFmpeg`，Windows用戶請參考[此篇文章](https://stackoverflow.com/questions/67713994/how-do-i-install-ffmpeg-for-my-bot-to-play-music)安裝並配置`FFmpeg`。

Linux用戶可以透過`snap`安裝。
```bash
sudo snap install ffmpeg
```
Unbuntu/Debian也可以用apt，不過我是用snap裝。其他發行板我不熟，請自己搜尋 :D

**倘若不需要語音功能亦可不安裝**。

## 配置文件
以下是配置配置文件說明。
## `.env`
該文件存放一些隱私資訊  
**請自行在專案根目錄下新增檔案`.env`並放入以下內容：**
```
gemini_api_key=your_gemini_api_key
weather_api_key=your_weather_api_key
discord_token=your_discord_api_key
```
並依需將`=`後面填上自己的資訊

`weather_api_key`為查詢氣象功能所需，採用**中央氣象局所提供之氣象資料API**。若無此需求，可**填入任意值**，但當你要求AI查詢氣象時會**出現報錯**
## `settings/settings.json`
該文件存放Discord bot與AI模型配置，可自行更改。  
標有`*`之設定更改需重新運行才會生效，其他設定可能需在Discord輸入`前綴+clear_chat`清除該輪對話才會生效。
### *`prefix`
bot的**指令前綴**。
### `model`
AI模型的**模型型號**。  
請參考Google提供之[文件](https://ai.google.dev/gemini-api/docs/models/gemini?hl=zh-tw)。
### `generation_config`
AI模型的**生成設定**。  
請參考Google提供之[文件](https://ai.google.dev/gemini-api/docs/text-generation?hl=zh-tw&lang=python#configure)。
### `safety_settings`
AI模型的**安全設定**。  
請參考Google提供之[文件](https://ai.google.dev/gemini-api/docs/safety-settings?hl=zh-tw)。
## `settings/system_prompt`
AI模型的系統提示詞，可以在其中指定AI扮演的角色或其他資訊。

預設為我寫的機器人`Oksana`之系統提示詞。
