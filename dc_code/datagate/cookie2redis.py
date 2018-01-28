"""
Not used
"""
import redis
import requests


def cookie2redis():
    # Initialize redis connection
    redis_conn = redis.StrictRedis(host="localhost", port=6379, db=9)

    # redis cookie expiration time
    time_out = 600  # seconds
    # url1 = "http://app1.sfda.gov.cn/datasearch/face3/base.jsp"
    url1 = "http://app1.sfda.gov.cn/datasearch/face3/base.jsp"
    url2 = "http://app1.sfda.gov.cn/datasearch/face3/base.jsp?security_verify_data=313932302c31303830"

    with requests.Session() as s:
        real_cookie = dict()

        cookie_dict = dict()
        while "yunsuo_session_verify" not in cookie_dict:
            print("1st")
            s.get(url1)
            cookie_dict = s.cookies.get_dict()
            print(cookie_dict)

        real_cookie["yunsuo_session_verify"] = cookie_dict["yunsuo_session_verify"]

        cookie_dict = dict()
        while "security_session_mid_verify" not in cookie_dict:
            print("2nd")
            s.get(url2)
            cookie_dict = s.cookies.get_dict()
            print(cookie_dict)

        real_cookie["security_session_mid_verify"] = cookie_dict["security_session_mid_verify"]

        cookie_dict = dict()
        while "JSESSIONID" not in cookie_dict:
            print("3rd")
            s.get(url1)
            cookie_dict = s.cookies.get_dict()

        real_cookie["JSESSIONID"] = cookie_dict["JSESSIONID"]

    cookie = "security_session_mid_verify={security_session_mid_verify}; yunsuo_session_verify={yunsuo_session_verify}; JSESSIONID={JSESSIONID}".format(**real_cookie)
    redis_conn.set('fda', cookie, time_out)


if __name__ == "__main__":
    cookie2redis()