import os
import requests
from bs4 import BeautifulSoup

db_file = "./file_update.txt"

def load_urls():
    """讀取已儲存的 URL、標題及其最後更新日期"""
    data = {}
    if os.path.exists(db_file):
        with open(db_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" ", 2)
                if len(parts) == 3:
                    data[parts[1]] = {"title": parts[0], "date": parts[2]}  # 標題: URL: 日期
    return data

def save_urls(data):
    """儲存 URL、標題及其最後更新日期"""
    with open(db_file, "w", encoding="utf-8") as f:
        for url, info in data.items():
            f.write(f"{info['title']} {url} {info['date']}\n")

def fetch_last_modified(url):
    """取得網站的最後更新日期，從畫面上的 '最近于' 後方取得日期"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 嘗試從畫面上的 '最近于' 後取得日期
        text = soup.get_text()
        if "最近于" in text:
            parts = text.split("最近于")
            if len(parts) > 1:
                date = parts[1].split()[0]  # 取得 '最近于' 後第一個單詞作為日期
                return date
        
        return "Unknown"
    except requests.RequestException:
        return "ERROR"

def main():
    urls_data = load_urls()
    new_data = {}
    changed_urls = []
    
    for url, info in urls_data.items():
        new_date = fetch_last_modified(url)
        if new_date != "ERROR":
            new_data[url] = {"title": info["title"], "date": new_date}
            if info["date"] != new_date:
                changed_urls.append((info["title"], url))
    
    save_urls(new_data)
    
    if changed_urls:
        print("以下網站內容已更新:")
        for title, url in changed_urls:
            print(f"{title} ({url})")
    else:
        print("無更新內容")

if __name__ == "__main__":
    main()
