#!/usr/bin/python
# coding=utf-8

#
#   Elliptic Curve Digital Signature Algorithm (ECDSA)
#
#   COPYRIGHT (c) 2010 by Toni Mattis <solaris@live.de>
#
import hashlib
from os import urandom
from elliptic import inv, mulf, mulp, muladdp, element
from curves import get_curve, implemented_keys

# y**2 == x**3 - p*x - q (mod n)
def randkey(bits, n):
    '''Generate a random number (mod n) having the specified bit length'''
    #随机数生成函数用
    rb = urandom(int(bits / 8) + 8)  # + 64 bits as recommended in FIPS 186-3
    #它是用来获取一个指定长度的bytes对象, 它实际上是在获取不同操作系统特定提供的随机源。
    c = 0
    for r in rb:
        c = (c << 8) | r #|执行按位或运算
    return (c % (n - 1)) + 1 #取模运算使随机数回到有限域范围内


def keypair(bits):
    '''Generate a new keypair (qk, dk) with dk = private and qk = public key'''
    #用于生成密钥对
    try:
        bits, cn, n, cp, cq, g = get_curve(bits) #相关函数位置在./ecc/curves.py文件里获得的参数分别为加密位数，大素数，该参数尚不明确其用途在于计算参数q，
        # 参数p,参数q,基点坐标
    except KeyError:
        raise ValueError("Key size %s not implemented" % bits)
    if n > 0:
        d = randkey(bits, n)
        q = mulp(cp, cq, cn, g, d)
        return (bits, q), (bits, d)
    else:
        raise ValueError("Key size %s not suitable for signing" % bits)


def supported_keys():
    '''Return a list of all key sizes implemented for signing'''
    return implemented_keys(True)


def validate_public_key(qk):
    '''Check whether public key qk is valid'''
    #对公钥进行验证
    bits, q = qk
    x, y = q
    bits, cn, n, cp, cq, g = get_curve(bits)
    return q and 0 < x < cn and 0 < y < cn and \
        element(q, cp, cq, cn) and (mulp(cp, cq, cn, q, n) == None)#element来自./ecc/elliptic 用来判断基点是否在曲线上


def validate_private_key(dk):
    '''Check whether private key dk is valid'''
    #对私钥进行验证
    bits, d = dk
    bits, cn, n, cp, cq, g = get_curve(bits)
    return 0 < d < cn


def match_keys(qk, dk):
    '''Check whether dk is the private key belonging to qk'''
    #检查公私钥之间的关联
    bits, d = dk
    bitz, q = qk
    if bits == bitz:
        bits, cn, n, cp, cq, g = get_curve(bits)
        return mulp(cp, cq, cn, g, d) == q
    else:
        return False


def truncate(h, hmax):
    '''Truncate a hash to the bit size of hmax'''
    #哈希截断
    while h > hmax:
        h >>= 1
    return h


def sign(h, dk):
    '''Sign the numeric value h using private key dk'''
    #数字签名算法
    bits, d = dk
    bits, cn, n, cp, cq, g = get_curve(bits)
    h = truncate(h, cn)
    r = s = 0
    while r == 0 or s == 0:
        k = randkey(bits, cn)
        kinv = inv(k, n) #inv源自./ecc/elliptic 用来计算模反元素
        kg = mulp(cp, cq, cn, g, k)
        r = kg[0] % n
        if r == 0:
            continue
        s = (kinv * (h + r * d)) % n
    return r, s


def verify(h, sig, qk):
    '''Verify that 'sig' is a valid signature of h using public key qk'''
    #使用公钥验签
    bits, q = qk
    try:
        bits, cn, n, cp, cq, g = get_curve(bits)
    except KeyError:
        return False
    h = truncate(h, cn)
    r, s = sig
    if 0 < r < n and 0 < s < n:
        w = inv(s, n)
        u1 = (h * w) % n
        u2 = (r * w) % n
        x, y = muladdp(cp, cq, cn, g, u1, q, u2)
        return r % n == x % n
    return False


def hash_sign(s, dk, hashfunc='sha256'):
    #利用哈希函数进行签名
    h = int(hashlib.new(hashfunc, s).hexdigest(), 16)
    return (hashfunc,) + sign(h, dk)


def hash_verify(s, sig, qk):
    #哈希验签
    h = int(hashlib.new(sig[0], s).hexdigest(), 16)
    return verify(h, sig[1:], qk)


if __name__ == '__main__':

    import time

    testh1 = 0x0123456789ABCDEF
    testh2 = 0x0123456789ABCDEE

    for k in supported_keys():
        qk, dk = keypair(k)
        s1 = sign(testh1, dk)
        s2 = sign(testh1, (dk[0], dk[1] ^ 1))
        s3 = (s1[0], s1[1] ^ 1)
        qk2 = (qk[0], (qk[1][0] ^ 1, qk[1][1]))

        assert verify(testh1, s1, qk)       # everything ok -> must succeed
        assert not verify(testh2, s1, qk)   # modified hash       -> must fail
        assert not verify(testh1, s2, qk)   # different priv. key -> must fail
        assert not verify(testh1, s3, qk)   # modified signature  -> must fail
        assert not verify(testh1, s1, qk2)  # different publ. key -> must fail

    def test_perf(bits, rounds=50):
        '''-> (key generations, signatures, verifications) / second'''
        h = 0x0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF
        d = get_curve(bits)

        t = time.time()
        for i in xrange(rounds):
            qk, dk = keypair(bits)
        tgen = time.time() - t

        t = time.time()
        for i in xrange(rounds):
            s = sign(0, dk)
        tsign = time.time() - t

        t = time.time()
        for i in xrange(rounds):
            verify(0, s, qk)
        tver = time.time() - t

        return rounds / tgen, rounds / tsign, rounds / tver
