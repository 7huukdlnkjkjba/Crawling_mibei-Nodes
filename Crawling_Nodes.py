import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

# 获取今天日期
today = datetime.now().strftime('%Y年%m月%d日')
main_url = 'https://www.mibei77.com/'

# 常见 User-Agent 列表
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/113.0"
]

def get_random_headers():
    return {
        "User-Agent": random.choice(user_agents)
    }

try:
    # 请求米贝主页
    response = requests.get(main_url, headers=get_random_headers(), timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 匹配以今天日期开头且包含“免费精选节点”的链接
    first_link = None
    for a_tag in soup.find_all('a', href=True):
        link_text = a_tag.get_text(strip=True)
        if link_text.startswith(today) and "免费精选节点" in link_text:
            first_link = a_tag['href']
            break

    if not first_link:
        print("未找到今日免费精选节点链接")
        sys.exit(1)

    print(f"今日免费精选节点页面: {first_link}")
    # 请求该页面
    sub_response = requests.get(first_link, headers=get_random_headers(), timeout=10)
    sub_response.raise_for_status()

    # 提取第一个符合规则的 .txt 节点链接
    txt_pattern = re.compile(r'http[s]?://mm\.mibei77\.com/\d{6}/[\w\.]+\.txt', re.IGNORECASE)
    txt_links = txt_pattern.findall(sub_response.text)

    if not txt_links:
        print("未找到 .txt 节点链接")
        sys.exit(1)

    # 下载第一个匹配的 .txt 节点文件
    node_url = txt_links[0]
    print(f"正在下载节点文件: {node_url}")
    node_response = requests.get(node_url, headers=get_random_headers(), timeout=10)
    node_response.raise_for_status()

    # 保证 config.txt 始终保存在源码目录
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, "config.txt")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(node_response.text)
    print(f"节点文件已保存到 {save_path}")

except Exception as e:
    print(f"获取节点失败: {type(e).__name__}: {e}")