import re
import requests
from bs4 import BeautifulSoup

def extract_urls(text):
  url_pattern = r'https://[^\s]+'
  urls = re.findall(url_pattern, text)
  return urls

def get_html(url):
  response = requests.get(url)
  html_content = response.text
  soup = BeautifulSoup(html_content, 'lxml')
  body_content = soup.body
  return body_content