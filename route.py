#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
import Queue
import csv

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) != 3:
        print "Usage: $ python %s from to" % argv[0]
        quit()
    category = {}
    alchemy = {}

    reader = csv.reader(open('./acquaintance.csv'))
    for data in reader:
        # print ', '.join(data)
        name = data[0]
        group = data[1]

        for i in xrange(4):
            if data[i * 2 + 2] != '':
                category[name] = category.get(name, [])
                category[name].append(data[i * 2 + 2])
        for i in xrange(4):
            if data[i * 2 + 10] != '':
                alchemy[data[i * 2 + 10]] = alchemy.get(data[i * 2 + 10], [])
                alchemy.get(data[i * 2 + 10], []).append(name)
    # print category
    if argv[1] not in category:
        print "%s は未登録の物質です" % argv[1]
        quit()
    if argv[2] not in category:
        print "%s は未登録の物質です" % argv[2]
        quit()

    G = []
    que = Queue.Queue()
    que.put([argv[1]])
    res = []
    while not que.empty():
        p = que.get()
        if p[0] == argv[2]:
            res = p
            break
        if len(p) > 7:
            continue
        for item in alchemy.get(p[0], []):
            pp = list(p)
            pp[0] = "%s %s" % (pp[0], pp[0])
            pp.insert(0, item)
            if item not in G:
                G.append(item)
                que.put(pp)
        for ctgr in category.get(p[0], []):
            for item in alchemy.get(ctgr, []):
                pp = list(p)
                pp[0] = "%s %s" % (pp[0], ctgr)
                pp.insert(0, item)
                if item not in G:
                    G.append(item)
                    que.put(pp)
    if len(res) == 0:
        print "結果を見つけることが出来ませんでした."
    for v in reversed(res):
        print v
