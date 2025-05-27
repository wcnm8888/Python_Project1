import json
import logging
import os
import ast
import threading
from queue import Queue
from time import sleep
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# === 日志配置 ===
logging.basicConfig(
    filename='error.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === 准备保存目录 ===
if not os.path.exists('datas'):
    os.makedirs('datas')

# === 线程数设置 ===
THREAD_COUNT = 4
TASK_QUEUE = Queue()

# === 读取 Cookie（所有线程共享） ===
with open('cookies.json', 'r', encoding='utf-8') as f:
    COOKIE_DATA = json.load(f)

# === 线程工作函数 ===
def worker(thread_id):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service('../../chromedriver.exe'), options=chrome_options)

    try:
        driver.get("https://bbs.nga.cn/?rand=921")
        for cookie in COOKIE_DATA:
            driver.add_cookie(cookie)
        driver.refresh()
        sleep(2)
        driver.find_element(By.LINK_TEXT, '程序员职业交流').click()
    except Exception as e:
        logging.error(f"[线程 {thread_id}] 初始化失败: {e}")
        driver.quit()
        return

    while not TASK_QUEUE.empty():
        try:
            index, title, link = TASK_QUEUE.get()
            logging.info(f"[线程 {thread_id}] 处理：{title} - {link}")
            driver.get(link)
            sleep(2)

            response = driver.page_source
            html = etree.HTML(response)

            content = html.xpath('//p[@class="postcontent ubbcode"]/text()')
            content = content[0].strip() if content else ""

            times = html.xpath('//span[@class=" postinfot postdatec stxt"]/text()')
            post_time = times[0].strip() if times else None
            mtime = [t.strip() for t in times[1:]]

            uid = html.xpath('//*[@id="posterinfo0"]/div[1]/a[2]/text()')
            uid = uid[0].strip() if uid else None
            ids = html.xpath('//*[@class="posterinfo"]/div[1]/a[2]/text()')
            mid = [i.strip() for i in ids[1:]]

            texts = []
            contents = html.xpath('//span[@class="postcontent ubbcode"]')
            for c in contents:
                quotes = c.xpath('.//div[@class="quote"]')
                for q in quotes:
                    q.getparent().remove(q)
                text = c.xpath('string(.)').strip()
                texts.append(text)
            mcontent = texts

            replies = []
            for j in range(len(mid)):
                replies.append({
                    "mid": mid[j] if j < len(mid) else None,
                    "mtime": mtime[j] if j < len(mtime) else None,
                    "mcontent": mcontent[j] if j < len(mcontent) else None
                })

            post_data = {
                "link": link,
                "title": title,
                "post_time": post_time,
                "uid": uid,
                "content": content,
                "replies": replies
            }

            filename = f'datas/post-{index}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(post_data, f, ensure_ascii=False, indent=4)

            logging.info(f"[线程 {thread_id}] 已保存 {filename}")

        except Exception as e:
            logging.error(f"[线程 {thread_id}] 处理失败: {e}")
        finally:
            TASK_QUEUE.task_done()

    driver.quit()
    logging.info(f"[线程 {thread_id}] 退出")

# === 主程序入口 ===
if __name__ == '__main__':
    try:
        with open('link.txt', 'r', encoding='utf-8') as f:
            links = f.readlines()

        for i, line in enumerate(links, 1):
            try:
                data = ast.literal_eval(line.strip())
                title = data[0]
                link = data[1]
                TASK_QUEUE.put((i, title, link))
            except Exception as e:
                logging.warning(f"解析链接失败：{line} -> {e}")

        threads = []
        for i in range(THREAD_COUNT):
            t = threading.Thread(target=worker, args=(i + 1,))
            t.start()
            threads.append(t)

        TASK_QUEUE.join()

        for t in threads:
            t.join()

        logging.info("所有线程已完成")

    except Exception as e:
        logging.critical(f"程序运行错误：{e}")
