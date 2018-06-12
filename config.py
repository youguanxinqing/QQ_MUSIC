# 请求头
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "c.y.qq.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
}

# API接口
HOT_URL = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?"

# GET参数
HOT_PARAMS = {
    "g_tk": "5381",
    "uin": "0",
    "format": "json",
    "inCharset": "utf-8",
    "outCharset": "utf-8",
    "notice": "0",
    "platform": "h5",
    "needNewCode": "1",
    "cid": "205360772",
    "reqtype": "1",
    "cmd": "6",
    "needmusiccrit": "0",
    "pagesize": "10",
    "lasthotcommentid": "",
    "qq": "0",
    "msg_comment_id": "",
    "pagenum": "0",
    "biztype": "1",
    "topid": "212606735",
    "ct": "888",
    "_": "1528784221616",
}

# 对应HOT_PARAMS中的lasthotcommentid
LAST_COMMENT_ID = ""

# 数据库配置
LOCALHOST = "localhost"
PORT = 3306
USER = "Guan"
PASSWORD = "guanyixin"
DB = "comment"