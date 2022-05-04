# edited on 2022.04.21
# Run with root in linux!!!

import time
import datetime
import requests
import subprocess
import random

username="2212026"
password="snda10086@"

def random_campusnet_choose(randomstr):
    redirect_url="https://portalnew"+randomstr+".dhu.edu.cn/switch.php?switchip=10.10.90.2&ip=10.199.176.227&url=http://1.2.3.4/&wlanacname=Bras_M6K_DH"
    login_url="https://portalnew"+randomstr+".dhu.edu.cn/post.php"
    post_data={
                "username":username,
                "password":password,
                "savePWD":"on"
    }
    post_header = {
        "Host": "portalnew"+randomstr+".dhu.edu.cn",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://portalnew"+randomstr+".dhu.edu.cn/portalcloud/page/2/PC/chn/Login.html?switchip=10.10.90.2&ip=10.199.176.227&url=http://1.2.3.4/&wlanacname=Bras_M6K_DH",
    }
    return redirect_url,login_url,post_data,post_header

test_url="https://www.baidu.com"

while True:
    session = requests.session()
    try:
        req=session.get(test_url,timeout=5)
        print(str(datetime.datetime.now())+" Network is fine.Next check will start in 120 seconds")
        time.sleep(120)
    except:
        try:
            print(str(datetime.datetime.now())+" Network disconnected, will start to reconnect.")
            redirect_url,login_url,post_data,post_header=random_campusnet_choose(random.choice(["","2","3"]))
            time.sleep(1)
            print("This time reconnecting will choose: {}".format(login_url))
            # only this step can get the true cookies.
            cookies=session.get(redirect_url,data=post_data,headers=post_header,cookies={"myusername": username,"pwd": password},allow_redirects=False)
            print("True cookies is: "+str(cookies.headers["Set-Cookie"]).split(" ")[0].split("=")[1])
            time.sleep(1)
            login=session.post(login_url,data=post_data,headers=post_header,cookies={"PHPSESSID":str(cookies.headers["Set-Cookie"]).split(" ")[0].split("=")[1]})
            print(session.cookies)
            print(str(datetime.datetime.now())+" Reconnect done.")
            time.sleep(30)
        except:
            print("Campus Network can not connect.")
            print("Try reload eth1.")
            ''' Discarded
            p = subprocess.Popen("su", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            time.sleep(2)
            p.stdin.write("room5135".encode("utf-8"))
            time.sleep(3)
            p.stdin.write("nmcli c reload".encode("utf-8"))
            time.sleep(3)
            p.stdin.write("nmcli c up eth1".encode("utf-8"))
            time.sleep(1)
            p.stdin.write("nmcli d reapply eth1".encode("utf-8"))
            time.sleep(10)
            '''
            # Run with root!
            step1=subprocess.run("nmcli c reload",shell=True,stdout=subprocess.PIPE).stdout.decode("utf-8")
            print(step1)
            time.sleep(1.5)
            step2=subprocess.run("nmcli c up eth1",shell=True,stdout=subprocess.PIPE).stdout.decode("utf-8")
            print(step2)
            time.sleep(1.5)
            step3=subprocess.run("nmcli d reapply eht1",shell=True,stdout=subprocess.PIPE).stdout.decode("utf-8")
            print(step3)
            time.sleep(10)


