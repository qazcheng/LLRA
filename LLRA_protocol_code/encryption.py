# coding:utf-8
import base64
from Crypto.Cipher import AES  # 注：python3 安装 Crypto 是 pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome<br><br>
import hashlib

def sha256(message):
    if(type(message)==int):
        message=str(message)
    h=hashlib.sha256()
    h.update(message.encode('utf-8'))
    return h.hexdigest()
def sha384(message):
    if(type(message)==int):
        message=str(message)
    h=hashlib.sha384()
    h.update(message.encode('utf-8'))
    return h.hexdigest()
def md5(message):
    if(type(message)==int):
        message=str(message)
    h=hashlib.md5()
    h.update(message.encode('utf-8'))
    return h.hexdigest()
def sha1(message):
    if(type(message)==int):
        message=str(message)
    h=hashlib.sha384()
    h.update(message.encode('utf-8'))
    # return str(int(h.hexdigest(),16))
    return h.hexdigest()

#解密
# def aes_decode(data, key):
#     try:
#         key = key[:32]  # 将密钥截断为32字节（256位）
#         aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
#         decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf8'))).decode("utf8")  # 解密
#         decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
#         return decrypted_text
#     except Exception as e:
#         print("AES解密出现错误:", str(e))
#         return None
# 解密
def aes_decode(data, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    # 先进行base64解码
    decrypted = base64.b64decode(data)
    # 解密数据并去除补位字符
    result = cipher.decrypt(decrypted).decode('utf-8')
    return result[:-ord(result[-1])]

# 加密
def aes_encode(data, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    # 数据长度不足16位，需要进行补位操作
    length = 16 - (len(data) % 16)
    data += chr(length) * length
    # 加密数据并进行base64编码
    encrypted = cipher.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def base64_e(data):
    data = str.encode(data)
    message=base64.encodebytes(data)
    return message
def base64_d(data):
    data = str.encode(data)
    message = base64.decodebytes(data)
    return message
def write_data_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)
def read_data_from_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data
# if __name__ == '__main__':
#     key = '12345678g01234ab'  # 密钥长度必须为16、24或32位，分别对应AES-128、AES-192和AES-256
#     data = "E83A56F6BCF88E5BD3600C398E39EAAFA91DBA24807B73F7B76FF1E180CEA14DAED6A43F9304901044C50503198C2D3A57661"  # 待加密文本
#
#     mi = aes_encode(data, key)
#     print("加密值：", mi)
#     print("解密值：", aes_decode(mi, key))
if __name__ == '__main__':
    key = '12345678g01234ab'  # 密钥长度必须为16、24或32位，分别对应AES-128、AES-192和AES-256
    data1 = "I LOVE YOU"  # 待加密文本
    data2=sha1(data1)#sha1加密
    data3=md5(data1)#md5加密
    mi = aes_encode(data1, key)#aes加密
    print("哈希值（sha1）：",data2)
    print("哈希值（md5）：", data3)
    # print("加密值：", mi)
    # print("解密值：", aes_decode(mi, key))