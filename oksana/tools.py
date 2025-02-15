from datetime import datetime, timedelta
import pytz
import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["weather_api_key"]

def load_file(name):
  with open(f'{name}', mode='r', encoding="utf8") as File:
      content = File.read()
  return content

def load_json(name):
  with open(f'{name}.json', mode='r', encoding="utf8") as jFile:
      jdata = json.load(jFile)
#  print(f'[{name}.json] 讀取！')
  jFile.close()
  return jdata

def write_js(name,data):
  jsdata = json.dumps(data,ensure_ascii=False)
  with open(f'{name}.json', mode='w', encoding="utf8") as jFile:
    jFile.write(jsdata)
    jFile.close()
#    print(f'[{name}.json] 寫入！')

def get_time():
    """
    獲取當前時間(Taiwan, GMT+8)
    回傳：以「年/月/日,時：分」為格式的字串
    """
    tz_taiwan = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz_taiwan)
    return now.strftime("%Y/%m/%d,%H:%M")

import requests
from typing import Literal


time_type = Literal["d","w"]
name_type = Literal[
    "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣",
    "臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市",
    "基隆市", "新竹縣", "新竹市", "苗栗縣", "彰化縣", "南投縣",
    "雲林縣", "嘉義縣", "嘉義市", "屏東縣"
]

def get_weather(time:time_type, locationName:name_type):
    """
    回傳未來的天氣
    參數:
      time: 想要看到的時間，請傳入d或w。
        d代表今、明天36小時的氣象報告
        w代表未來一週的氣象預報
      locationName: 傳入縣市名稱，允許的參數如下：
        [宜蘭縣, 花蓮縣, 臺東縣, 澎湖縣, 金門縣, 連江縣, 臺北市, 新北市, 桃園市, 臺中市, 臺南市, 高雄市, 基隆市, 新竹縣, 新竹市, 苗栗縣, 彰化縣, 南投縣, 雲林縣, 嘉義縣, 嘉義市, 屏東縣]
    """
    url1 = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={TOKEN}&locationName={locationName}"
    url2 = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization={TOKEN}&locationName={locationName}"
    url = {"d":url1, "w":url2}.get(time)
    res = requests.get(url)
    return res.json()["records"]

def get_stock_price(code:str):
    """
    取得股票的股價
    傳入股票代碼，限定台股，例如查台積電就傳入2330
    """
    url = f'https://tw.stock.yahoo.com/quote/{code}'
    web = requests.get(url)
    soup = BeautifulSoup(web.text, "html.parser")
    title = soup.find('h1')
    name = soup.select('.Fz\(24px\)')[0]
    a = soup.select('.Fz\(32px\)')[0]
    return a.get_text()

def get_stock_saleInfo(code:str):
    """
    取得這隻股票的營收資訊
    傳入股票代碼，限定台股，例如查台積電就傳入2330
    """
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-TW,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Content-Length': '0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://goodinfo.tw',
            'Referer': f'https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID={code}',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
        cookies = {

            'IS_TOUCH_DEVICE': 'F',
            'SCREEN_SIZE': 'WIDTH=1280&HEIGHT=720',
        }
        url = f'https://goodinfo.tw/tw/ShowSaleMonChart.asp?STOCK_ID={code}&INIT=T'
        web = requests.post(url=url, headers=headers,cookies=cookies)
        soup = BeautifulSoup(web.text, 'html.parser')
    #       print(soup)
        tb = soup.find('tr',id='row0')
    #        print(tb)
        cells = tb.find_all('td')
        data = {
                    '日期': cells[0].text,
                    "營收": cells[7].get_text(strip=True) + " 億元新台幣",
                    "月增": cells[8].get_text(strip=True),
                    "年增": cells[9].get_text(strip=True),
            "累計年增": 
        cells[11].get_text(strip=True)
                }
        print(f'{code}：{data}')
        return data

    except Exception as e:
        print(e)
        return e

def get_stock_info(code:str):
    """
    取得這隻股票的詳細資訊，傳入股票代碼
    限定台股，範例：如果要查台積電，傳入2330
    """
    url = f'https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID={code}'
    data = {
        'code':code
    }
    headers = {
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
    cookies = {
        'IS_TOUCH_DEVICE': 'F',
        'SCREEN_SIZE': 'WIDTH=1280&HEIGHT=720',
    }
    web = requests.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(web.content, 'html.parser')
#    print(soup)
    array = []
    name = soup.find('table',class_='b1 p6_0 r10_0 box_shadow').find('b').find('nobr').get_text()
    data['name'] = name[5:]
    time_ = soup.find('table',id='tblFinDetail').find('tr',class_='bg_h1 fw_normal').find_all('nobr')
    gross_profit = soup.find('tr',id='row0').find_all('nobr')
    profit = soup.find('tr',id='row1').find_all('nobr')
    profit_bt = soup.find('tr',id='row2').find_all('nobr')
    profit_at = soup.find('tr',id='row3').find_all('nobr')
    stock_p_bt = soup.find('tr',id='row5').find_all('nobr')
    stock_p_at = soup.find('tr',id='row6').find_all('nobr')
    stock_v = soup.find('tr',id='row7').find_all('nobr')
    array.append(time_)
    array.append(gross_profit)
    array.append(profit)
    array.append(profit_bt)
    array.append(profit_at)
    array.append(stock_p_bt)
    array.append(stock_p_at)
    array.append(stock_v)

    url = f'https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID={code}'
    web = requests.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(web.content, 'html.parser')
    total =  [soup.find('tr',string='資產總額'),soup.find('td',string='資產總額').find_next_sibling()]
    debt =  [soup.find('tr',string='負債總額'),soup.find('td',string='負債總額').find_next_sibling()]
    array.append(total)
    array.append(debt)

    url = f'https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=IS_M_QUAR_ACC&STOCK_ID={code}'
    web = requests.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(web.content, 'html.parser')
    profit = [soup.find('td',string='營業收入')]
    profit += soup.find('td',string='營業收入').find_next_siblings('td')
    array.append(profit)
    print(profit)

    url = f'https://goodinfo.tw/tw/BasicInfo.asp?STOCK_ID={code}'
    web = requests.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(web.content, 'html.parser')
    cs1 = soup.find('td',string='資本額').get_text()
    cs = soup.find('td',string='資本額').find_next_sibling().get_text()
    data[cs1] = cs

    url = f'https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID={code}'
    web = requests.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(web.content, 'html.parser')
    stock_p = soup.find('tr',id='row1').find_all('td')
    data['現金股利'] = []
    for i in stock_p[1:4]:
        data['現金股利'].append(i.get_text())

    for i in array:
        for j in i:
            array[array.index(i)][array[array.index(i)].index(j)] = j.get_text()
    for i in array:
        data[i[0]] = i[1:]

    sale_info = get_stock_saleInfo(code)
    for key,value in sale_info.items():
        data[key] = value
    return data
