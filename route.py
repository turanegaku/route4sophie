#!/usr/bin/env python
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
    for data in list(reader)[1:]:
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

    que = Queue.Queue()
    que.put([argv[1]])
    while True:
        minv = 100
        while not que.empty():
            p = que.get()
            if len(p) > minv:
                que.put(p)
                break
            if p[0] == argv[2]:
                minv = min(minv, len(p))
                print ' '.join(reversed(p))
            for item in alchemy.get(p[0], []):
                if item in p:
                    continue
                pp = list(p)
                pp.insert(0, "\033[94m" + pp[0] + "\033[0m")
                pp.insert(0, item)
                que.put(pp)
            for ctgr in category.get(p[0], []):
                for item in alchemy.get(ctgr, []):
                    if item in p:
                        continue
                    pp = list(p)
                    pp.insert(0, "\033[94m" + ctgr + "\033[0m")
                    pp.insert(0, item)
                    que.put(pp)
        if minv == 100:
            print "結果を見つけることが出来ませんでした."
            break
        else:
            print 'show more? [y/n]:',
            try:
                if raw_input() != 'y':
                    break
            except KeyboardInterrupt:
                break
