import requests
import re
from config import *
import json
import time
import pymysql


# 链接数据库
conn = pymysql.connect(host=LOCALHOST, port=PORT, user=USER, \
                       password=PASSWORD, db=DB, charset="utf8mb4")
# 光标对象
cursor = conn.cursor()

def get_html(url, headers, params=None, tries=3):
    """
    获取html,精确说，应该是json数据
    :param url:
    :param headers:
    :param params:
    :param tries:
    :return:
    """
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        response.encoding = "utf-8"
    except requests.HTTPError:
        print("connect error")
        # 如果连接失败，重连三次
        if tries>0:
            print("reconnect...")
            get_html(BASE_URL, HEADERS, BASE_PARAMS, tries-1)
        # 失败三次则返回空，并打印提示语
        else:
            print("3 times failure")
            return None

    return response

def paras_html(html):
    data = {}
    content = json.loads(html)
    # 提取数据
    if content and "comment" in content.keys():
        for item in content["comment"]["commentlist"]:
            data["nike"] = item.get("nick")
            # 做简单的数据清洗操作
            data["comment"] = re.sub(r"\\n", " ", item.get("rootcommentcontent"))
            data["comment"] = re.sub(r"\n", " ", data["comment"])
            data["praisenum"] = item.get("praisenum")
            data["comment_id"] = item.get("commentid")
            # 时间戳转格式
            data["time"] = time.strftime("%Y-%m-%d %H:%M:%S",\
                                         time.localtime(int(item.get("time"))))
            yield data

def to_mysql(data):
    """
    插入操作，存入数据库
    :param data:
    :return:
    """
    # 构造插入命令
    command = 'insert into qqmusic values(\
              "{0}", "{1}", "{2}", "{3}", "{4}", "{5}")'.format(\
        0, data["nike"].replace("'", "\'").replace('"',"\'"),\
        data["comment"].replace("'", "\'").replace('"', "\'"), \
        data["praisenum"], data["comment_id"], data["time"])
    print(command)
    try:
        cursor.execute(command)
    except TypeError as e:
        print(e)
    # 无意外提交数据
    conn.commit()

def main():

    failureLinks = [] # 存放首次失败链接
    abandonLinks = [] # 存放失败三次链接
    count = 0
    global LAST_COMMENT_ID
    for page in range(400):
        # 每5页休息2秒
        if page%5 == 0:
            time.sleep(2)

        # 动态改变请求头
        HOT_PARAMS["lasthotcommentid"] = LAST_COMMENT_ID
        HOT_PARAMS["_"] = int(time.time()*1000)
        HOT_PARAMS["pagenum"] = page

        # 如果存在失败链接，求情失败链接
        # 失败三次放弃，存入abandonLinks
        if failureLinks:
            if count>=3:
                abandonLinks.append(failureLinks.pop())
                continue
            count += 1
            response = get_html(failureLinks.pop(), HEADERS)
        else:
            count = 0
            response = get_html(HOT_URL, HEADERS, HOT_PARAMS)
        # 请求成功，处理数据
        if response:
            try:
                for item in paras_html(response.text):
                    # print(item)
                    to_mysql(item)
                    print("【SUCCESSFUL】",response.url)
                    LAST_COMMENT_ID = item["comment_id"]
            except TypeError:
                # 可能返回的不是目标数据，加入失败链接组
                print(response.url)
                failureLinks.append(response.url)
    # 关闭光标与数据库连接
    cursor.close()
    conn.close()
    # 最后打印遗留链接
    print(abandonLinks)


if __name__ == "__main__":
    main()
