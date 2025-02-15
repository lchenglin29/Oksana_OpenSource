# Discord AI Chatbot  
[繁體中文](/README.md) ｜ English

**⚠️This page is translated by AI.⚠️**
***
**Notice! Since there are some differences with the original repository, make sure to read this!**  
Also, this is the project documentation. For basic tutorials, you can refer to my tutorial or other articles.

I will list my articles and some great resources in the [Tutorial Resources](#tutorial-resources) section at the bottom.

# Introduction  
This is the **AI Discord chatbot I started building since high school**  
In order to create my learning portfolio, I’ve organized the code and make it easier for everyone to use.

As for the **original repository (Oksana_dev)**, the code was a bit messy, so **I’ve made it private**. However, if there are any major updates, I will likely update this repository too, so no worries!

Since I’m putting in so much effort, please give me a star! :D

# Overview  
This is a Discord bot developed using **Discord.py** and **Gemini API**  
* Features:
    * Mention the bot or reply to the bot’s message in a text channel to have a conversation with the AI
    * Can read **images** attached in messages
    * Supports voice functionality, allowing conversations in **voice channels**
    * Can check the **weather**(in Taiwan)
    * Can check **daily stock prices** and **company revenue info** (requires the stock code of the company you want to query)
    * Can **read web pages** when given a **link** in the message
    * You can write system prompts in `settings/system_prompt` to customize your AI

# Setup  
## Install Required Python Libraries  
Please run the following command in the terminal:  
```bash
pip install -r requirements.txt
```

## FFmpeg  
Since voice functionality requires `FFmpeg`, Windows users can refer to [this article](https://stackoverflow.com/questions/67713994/how-do-i-install-ffmpeg-for-my-bot-to-play-music) to install and configure `FFmpeg`.

Linux users can install it via `snap`.  
```bash
sudo snap install ffmpeg
```

> Ubuntu/Debian users can also use apt, but I installed it with snap. I’m not familiar with other distributions, so please search it yourself :D

> **If you don't need voice functionality, you can skip installing FFmpeg**.

## Configuration Files  
Below are the descriptions of the configuration files.

### `.env`  
This file stores sensitive information  
**Please create a `.env` file in the project root directory and add the following content:**  
```
gemini_api_key=your_gemini_api_key
weather_api_key=your_weather_api_key
discord_token=your_discord_api_key
```
Fill in the information after `=` as needed. For details on how to obtain these, refer to the [Tutorial Resources](#tutorial-resources).

> `weather_api_key` is required for the weather query feature, using the **Taiwan Central Weather Administration's weather data API**. If you don’t need this, you can **put any value** in, but requesting weather info will result in an **error**.

### `settings/settings.json`  
This file stores Discord bot and AI model configurations, which you can modify.  
Settings marked with `*` need a restart to take effect, while other settings may require using `prefix+clear_chat` in Discord to clear the current conversation for them to take effect.

#### *`prefix`  
Bot’s **command prefix**.  
Please refer to [Command Description](#commands).

#### `model`  
The **model type** for the AI.  
Refer to Google’s [documentation](https://ai.google.dev/gemini-api/docs/models/gemini?hl=en).

#### `generation_config`  
The **generation configuration** for the AI model.  
Refer to Google’s [documentation](https://ai.google.dev/gemini-api/docs/text-generation?hl=en&lang=python#configure).

#### `safety_settings`  
The **safety settings** for the AI model.  
Refer to Google’s [documentation](https://ai.google.dev/gemini-api/docs/safety-settings?hl=en).

### `voice_settings`  
AI voice settings  
Please refer to the [Edge-TTS documentation](https://github.com/rany2/edge-tts).

### `settings/system_prompt`  
The system prompt for the AI model, where you can specify the role or other information for the AI.

The default system prompt is for my bot `Oksana`.

# Commands  
I’ve written some basic ctx commands. The usage format is `bot_prefix+command_name <parameter>`.  
Example: using the default prefix and the `say` command (passing in a parameter):  
```
!say hi
```
You can use the `help` command to view the list of commands, and use `help <command>` to get detailed info on each command.

A more important command is `clear_chat`. Since the bot supports multi-turn conversations and stores conversation data by channel, if you want to end (clear) the current conversation, use the `clear_chat` command.

# Tutorial Resources  
* Basics of Discord bots and how to get a Discord bot token: [Python Discord Bot Basics Tutorial](https://hackmd.io/@smallshawn95/python_discord_bot_base)  
* How to obtain a Gemini API key: [Get Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key?hl=en)  
* How to obtain the Central Weather Bureau API key: [[Day 13 - Real-time Weather] Build a Real-time Weather App - Preparation](https://ithelp.ithome.com.tw/m/articles/10222662)