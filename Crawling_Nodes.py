import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 第一步：获取今天的日期，格式为“2025年04月21日”
today = datetime.now().strftime('%Y年%m月%d日')
main_url = 'https://www.mibei77.com/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

try:
    # 请求米贝主页
    response = requests.get(main_url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 只匹配以今天日期开头且包含“免费精选节点”的链接
    first_link = None
    for a_tag in soup.find_all('a', href=True):
        link_text = a_tag.get_text(strip=True)
        # 严格要求以今日日期开头并包含“免费精选节点”
        if link_text.startswith(today) and "免费精选节点" in link_text:
            first_link = a_tag['href']
            break

    if not first_link:
        print("未找到今日免费精选节点链接")
        exit(1)

    print(f"今日免费精选节点页面: {first_link}")
    # 请求该页面
    sub_response = requests.get(first_link, headers=headers, timeout=10)
    sub_response.raise_for_status()

    # 只提取第一个符合规则的 .txt 节点链接
    txt_pattern = re.compile(r'http[s]?://mm\.mibei77\.com/\d{6}/[\w\.]+\.txt', re.IGNORECASE)
    txt_links = txt_pattern.findall(sub_response.text)

    if not txt_links:
        print("未找到 .txt 节点链接")
        exit(1)

    # 下载第一个匹配的 .txt 节点文件
    node_url = txt_links[0]
    print(f"正在下载节点文件: {node_url}")
    node_response = requests.get(node_url, headers=headers, timeout=10)
    node_response.raise_for_status()

    # 保存到脚本同目录下的 config.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, "config.txt")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(node_response.text)
    print(f"节点文件已保存到 {save_path}")

except Exception as e:
    print(f"获取节点失败: {e}")