#3,Verificator, тип: localmath. Экспортируемые математические функции
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Программно-аппаратный комплекс "Автоматизация проведения поверочных процедур метрологического оборудования"
# (с) НПО "Химавтоматика", 2009 - 2011
#
# Экспортируемые математические функции


from __future__ import division
from math import *
import __builtin__

class Jail(object):
    def __init__ (self):
        pass

def sanitize(expr):
    result = ''
    expr = str(expr).strip()
    if not len(expr):
        result = 'O'
        return result
    for c in expr:
        if c == ',':
            result += '.'
        elif c == '':
            pass
        else:
            result += c
    return result

def _convertargs(iter, *args):
    if len(args):
        list = (iter,)+args
    elif hasattr (iter,'__getitem__'):
        list = iter
    else:
        list = (iter,)
        list = [x/1 if type(x) == int else x for x in list]
    return list

def max(iter, *args):
    return __builtin__.max(_convertargs(iter, *args))

def min(iter, *args):
    return __builtin__.min(_convertargs(iter, *args))

def avg(iter, *args):
    list = _convertargs(iter, *args)
    return sum(list) / len(list)

def msdev(iter, *args):
    list = _convertargs(iter, *args)
    m = avg(list)
    n = len(list)
    sum = 0.0
    for i in range (len(list)):
        sum += (list[i]-m) ** 2
        sum /= n
        sum = sqrt(sum)
    return sum

def ssdev(iter, *args):
    list = _convertargs(iter, *args)
    m = avg(list)
    n = len(list)
    sum = 0.0
    if n == 1:
        return sum
    for i in range (len(list)):
        sum += (list[i]-m) ** 2
        sum /= (n-1)
        sum = sqrt(sum)
    return sum

def rangedev(iter, *args):
    list = _convertargs(iter, *args)
    return max(list)-min(list)

def sqavg(iter, *args):
    list = _convertargs(iter, *args)
    n = len(list)
    sum = 0.0
    for i in range (len(list)):
        sum += list[i] ** 2
        sum /= n
        sum = sqrt(sum)
    return sum