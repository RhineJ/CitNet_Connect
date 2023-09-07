import requests
import time
import json
#username 后面填写账号
userName = '19990582191'
#pwva1 后面填写密码
pwdVal = '123456'


def do_encrypt_rc4(src, passwd):
    src = src.strip()
    passwd = str(passwd)
    plen = len(passwd)
    size = len(src)
    key = [ord(passwd[i % plen]) for i in range(256)]
    sbox = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + sbox[i] + key[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
    a = b = c = 0
    output = []
    for i in range(size):
        a = (a + 1) % 256
        b = (b + sbox[a]) % 256
        sbox[a], sbox[b] = sbox[b], sbox[a]
        c = (sbox[a] + sbox[b]) % 256
        temp = ord(src[i]) ^ sbox[c]
        temp = hex(temp)[2:]
        if len(temp) == 1:
            temp = '0' + temp
        elif len(temp) == 0:
            temp = '00'
        output.append(temp)
    return ''.join(output)

auth_tag = str(int(time.time()))
pwd = do_encrypt_rc4(pwdVal, auth_tag)

print(pwd)

url = 'http://1.1.1.4/ac_portal/login.php'

form_data = {
    'opr': 'pwdLogin',
    'userName': userName,
    'pwd': pwd,
    'auth_tag': auth_tag,
    'rememberPwd': '0'
}

response = requests.post(url, data=form_data)

print(response.status_code)
print(response.text)

if response.status_code == 200:
    print("1")
    
if response.status_code == 200:
    response_text = response.text.replace("'", "\"")  # 将单引号替换为双引号
    try:
        response_data = json.loads(response_text)  # 手动解析响应内容
        if response_data.get('success'):
            print("连接成功")
            print("用户名:", response_data.get('userName'))
            print("位置:", response_data.get('location'))
        else:
            print("连接失败")
    except json.JSONDecodeError as e:
        print("无法解析JSON响应:", e)
else:
    print("连接失败，HTTP状态码:", response.status_code)