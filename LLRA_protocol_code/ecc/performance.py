#!/usr/bin/python
# coding=utf-8

import time

from collections import OrderedDict

from Key import Key


def test_generation_perf(n=100):
    #统计密钥生成所花费的时间
    results = OrderedDict() #建立有序字典
    for bits in (192, 224, 256, 384, 521):
        t = time.time()
        for i in range(n): # python 3.x中range等效于python 2中的xrange
            k = Key.generate(bits)
        t = time.time() - t
        results[bits] = t
    return results


def test_signing_perf(n=100):
    #统计数字签名花费的时间
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        k = Key.generate(bits)
        t = time.time()
        for i in range(n):
            k.sign('random string')
        t = time.time() - t
        results[bits] = t
    return results


def test_verification_perf(n=100):
    #统计验签的时间
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        k = Key.generate(bits)
        s = k.sign('random string')
        t = time.time()
        for i in range(n):
            k.verify('random string', s)
        t = time.time() - t
        results[bits] = t
    return results


def print_dict(title, d, n):
    #输出统计的有序字典
    print(title)
    print('-' * len(title))
    for k, v in d.items():
        print('{} bits  {:10.5f} seconds  {:10.5f}/sec'.format(k, v, n / v))
    print('')


if __name__ == '__main__':
    n = 100
    print_dict('Key generation', test_generation_perf(n), n)
    print_dict('Signing', test_signing_perf(n), n)
    print_dict('Verifying', test_verification_perf(n), n)
