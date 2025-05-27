import pymysql
import json
import os
from datetime import datetime

# 正确创建连接（不要再传给 connect 函数了）
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='nga'
)

def insert_post_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cursor = conn.cursor()

    # 插入主贴
    cursor.execute('''
        INSERT INTO posts (link, title, post_time, uid, content)
        VALUES (%s, %s, %s, %s, %s)
    ''', (
        data['link'],
        data['title'],
        parse_time(data['post_time']),
        data['uid'],
        data['content']
    ))

    post_id = cursor.lastrowid

    # 插入回复
    for reply in data.get('replies', []):
        cursor.execute('''
            INSERT INTO replies (post_id, mid, mtime, mcontent)
            VALUES (%s, %s, %s, %s)
        ''', (
            post_id,
            reply['mid'],
            parse_time(reply['mtime']),
            reply['mcontent']
        ))

    conn.commit()

def parse_time(t):
    try:
        return datetime.strptime(t, '%Y-%m-%d %H:%M')
    except:
        return None

def batch_insert(directory='datas'):
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    for filename in files:
        path = os.path.join(directory, filename)
        print(f'✅ 正在插入: {filename}')
        try:
            insert_post_from_json(path)
        except Exception as e:
            print(f'❌ 插入失败: {filename}, 错误: {e}')
    print('✅ 所有数据插入完成')

if __name__ == '__main__':
    batch_insert('./datas')
    conn.close()  # 最后关闭连接
