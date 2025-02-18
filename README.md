# Discord AI聊天機器人  
繁體中文 ｜ [English](/README/README_en.md)
***
**注意！因為跟原本的儲存庫有點差異，請一定要讀這篇！**
另外，此為專案說明文件，若需要基本教學可以參考我的教學或者其他文章。

我會將我的文章與我覺得很棒的資源放在最底下的[教學資源](#教學資源)。
# 前言
這是**我從高一開始製作的，可以在語音頻道跟你對話的AI Discord聊天機器人**  
為了做學習歷程所以將程式碼整理整理，順便處理了配置的東西，讓大家更好使用

關於**原本的儲存庫(Oksana_dev)**，因為code有點屎所以**被我關成私人了**，不過如果有重大更新我應該也會把這裡更新一遍所以不用太擔心

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
> Ubuntu/Debian也可以用apt，不過我是用snap裝。其他發行板我不熟，請自己搜尋 :D

> **倘若不需要語音功能亦可不安裝**。

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
並依需將`=`後面填上自己的資訊。關於如何取得可以參考[教學資源](#教學資源)

> `weather_api_key`為查詢氣象功能所需，採用**中央氣象局所提供之氣象資料API**。若無此需求，可**填入任意值**，但當你要求AI查詢氣象時會**出現報錯**
## `settings/settings.json`
該文件存放Discord bot與AI模型配置，可自行更改。  
標有`*`之設定更改需重新運行才會生效，其他設定可能需在Discord輸入`前綴+clear_chat`清除該輪對話才會生效。
### *`prefix`
bot的**指令前綴**。  
請參考[指令說明](#指令)。
### `model`
AI模型的**模型型號**。  
請參考Google提供之[文件](https://ai.google.dev/gemini-api/docs/models/gemini?hl=zh-tw)。
### `generation_config`
AI模型的**生成設定**。  
請參考Google提供之[文件](https://ai.google.dev/gemini-api/docs/text-generation?hl=zh-tw&lang=python#configure)。
### `safety_settings`
AI模型的**安全設定**。  
請參考Google提供之[文件](https://ai.google.dev/gemini-api/docs/safety-settings?hl=zh-tw)。
### `voice_settings`
AI語音的聲音設定。  
請參考Edge-tts之[說明文件](https://github.com/rany2/edge-tts)。
## `settings/system_prompt`
AI模型的系統提示詞，可以在其中指定AI扮演的角色或其他資訊。

預設為我寫的機器人`Oksana`之系統提示詞。
# 指令
我有寫了一些基本的ctx指令，使用方法為`bot前綴+指令名稱 <參數>`。  
範例，預設前綴+`say`指令(並傳入參數)：
```
!say hi
```
可以使用`help`指令查看指令列表，並用`help <指令>`查看該指令之詳細資訊。

比較重要的是`clear_chat`指令。由於bot支援多輪對話，且依照不同頻道儲存對話資訊，若要結束(清除)該輪對話資訊，請使用`clear_chat`指令。
# 教學資源
* Discord bot基礎與如何取得Discord bot token：[Python Discord Bot 基礎教學](https://hackmd.io/@smallshawn95/python_discord_bot_base)
* 取得Gemini API key：[取得 Gemini API 金鑰](https://ai.google.dev/gemini-api/docs/api-key?hl=zh-tw)
* 取得氣象局API key：[[Day 13 - 即時天氣] 建立一個即時天氣 App - 前置準備](https://ithelp.ithome.com.tw/m/articles/10222662)