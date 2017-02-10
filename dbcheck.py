#1. Verificator, тип: dbcheck. Утилита проверки целостности базы данных
#!/usr/bin/env python
# coding: utf-8
#
# Программно-аппаратный комплекс "Автоматизация проведения поверочных процедур метрологического оборудования"
# (с) НПО "Химавтоматика", 2009 - 2011
#
# Утилита проверки целостности базы данных

from __future__ import division
import sys, os, platform, keyword, re, tokenize, localmath
from elixir import *
from generate import *

theos=platform.system()
fsenc=sys.getfilesystemencoding()
frost=hasattr(sys, 'frozen')

if frost:
    filepath = os.path.dirname(unicode(sys.executable,fsenc))
    fileformat = u'скомпонованный'
elif __file__:
    filepath = os.path.dirname(__file__)
    fileformat = u'обычный'

datapath = os.path.join(filepath, 'verificator.db')
if theos == 'Windows':
    import win32api
    datapath=win32api.GetShortPathName(datapath)
    dataconnstr = "sqlite:///"+datapath.encode(fsenc)
    metadata.bind = dataconnstr

def isidentifier(candidate):
    is_not_keyword = candidate not in keyword.kwlist
    matches_pattern = re.match('^'+tokenize.Name+'$', candidate) is not None
    return is_not_keyword and matches_pattern

class internaldata(object):
    def __init__(self):
        pass

def main():
    print 'Verificator DB checker.'
    internal=internaldata()
    dt_total=0
    t_total=0
    g_total=0
    q_total=0
    qi_total=0
    e_total=0
    deviceTypes=DeviceType.query.all()
    for dt in deviceTypes:
        dt_total += 1
        print '.',
        params = dt.passport_parameters
    for p in params:
        print '.',
    if not isidentifier(p.variable_name):
        print '\nWrong variable name in (%s, %s, %s) parameter used in "%s"'(p.variable_name, p.description, p.readable_name, dt.model)
        e_total += 1
    else:
        exec(p.variable_name+'=1',vars(internal))
        tools = dt.required_tools
    for t in tools:
        t_total += 1
        print '.',
    questionGroups = dt.question_groups
    gnums = [g.num for g in questionGroups]
    gnums.sort()
    if len(gnums):
        dups=list(set(gnums))
        dups.sort()
    if dups != gnums:
        print '\nDuplicate numbers in "%s" group for "%s": %s' % (g.caption, dt.model, str(gnums))
        e_total += 1
    if range(gnums[0],gnums[-1]+1) != gnums:
        print '\nMissing numbers in "%s" group for "%s": %s' % (g.caption, dt.model, str(gnums))
        e_total += 1
    for g in questionGroups:
        g_total += 1
        print '.',
    questions=g.questions
    qnums = [q.num for q in questions]
    qnums.sort()
    if len(qnums):
        dups=list(set(qnums))
        dups.sort()
    if dups != qnums:
        print '\nDuplicate numbers in "%s" question in group "%s" for "%s": %s' % (q.caption, g.caption, dt.model, str(qnums))
        e_total += 1
    elif range(1,qnums[-1]+1) != qnums:
        print '\nMissing numbers or not started from 1 in "%s" question in group "%s" for "%s": %s' % (
        q.caption, g.caption, dt.model, str(qnums))
        e_total += 1
    for q in questions:
        q_total += 1
        plist=[]
        pclist=[]
        pnlist=[]
        phlist=[]
    if q.params != None and q.params != u'':
        plist = [param.strip() for param in q.params.split('$')]
    for p in plist:
        if not isidentifier(p):
            print '\nWrong variable name in "%s" parameter used in "%s" question in "%s" group for "%s"' % (p, q.caption, g.caption, dt.model)
            e_total += 1
        else:
            exec(p+'=1',vars(internal))
        if q.param_comments != None and q.param_comments != u'':
            pclist = [param.strip() for param in q.param_comments.split('$')]
        if len(plist) < len(pclist):
            print '\nNot enough parameters in "%s" question in "%s" group for "%s"' % (q.caption, g.caption, dt.model)
            e_total += 1
        if q.question_type.id == 1:
            if q.param_names != None and q.param_names != u'':
                pnlist = [param.strip() for param in q.param_names.split('$')]
            if q.param_hints != None and q.param_hints != u'':
                phlist = [param.strip() for param in q.param_hints.split('$')]
    for p in phlist:
        try:
            eval(p,vars(localmath),vars(internal))
        except NameError:
            print '\nUnknown variable in hint "%s" in "%s" question in "%s" group for "%s"' % (p, q.caption, g.caption, dt.model)
            e_total += 1
    if len(pclist) != len(pnlist) or len(pclist) != len(phlist):
        print '\nParameters mismatch in "%s" question in "%s" group for "%s"' % (q.caption, g.caption, dt.model)
        e_total += 1
    try:
        exec(q.calculation,vars(localmath),vars(internal))
    except NameError:
        print '\nUnknown variable in calculation "%s" in "%s" question in "%s" group fог "%s"' %(q.calculation, q.caption, g.caption, dt.model)
        e_total += 1
    if q.iterations:
        try:
            exec(q.condition,vars(localmath),vars(internal))
        except NameError:
            print '\nUnknown variable in condition "%s" in "%s" question in "%s" group for "%s"' %(q.condition, q.caption, g.caption, dt.model)
        e_total += 1
    else:
        try:
            eval(q.condition,vars(localmath),vars(internal))
        except (NameError, SyntaxError):
            print '\nUnknown variable in condition or incorrect condition',
            print '"%s" in "%s" question in "%s" group for "%s"' % (q.condition, q.caption, g.caption, dt.model)
        e_total += 1
    if q.iterations:
        qi_total += 1
    if q.calculation is not None and q.calculation != u'':
        print '\nIgnored calculation in iterative question "%s" in "%s" group for "%s"' % (q.caption, g.caption, dt.model)
        e_total += 1
        print '.',
        print '\nCheck complete.\nDefmed %u device types, %u tools,' % (dt_total, t_total),
        print '%u groups, %u questions (%u iterative), %u dynamic variables used.\nErrors found: %u' % (g_total, q_total, qi_total, len(dir(internal))-15, e_total)

    setup_all()
    main()
