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
    start = argv[1]
    goal = argv[2]
    category = {}
    categories = set()
    alchemy = {}

    reader = csv.reader(open('./acquaintance.csv'))
    for data in list(reader)[1:]:
        # print ', '.join(data)
        name = data[0]
        group = data[1]

        for item in [x for x in data[2:10:2] if x]:
            category[name] = category.get(name, [])
            category[name].append(item)
            categories.add(item)
        for item in [x for x in data[10:18:2] if x]:
            alchemy[item] = alchemy.get(item, [])
            alchemy.get(item, []).append(name)
    # print category
    if start not in category:
        print "%s は未登録の物質です" % start
        quit()
    if goal not in category and goal not in categories:
        print "%s は未登録の物質です" % goal
        quit()

    que = Queue.Queue()
    que.put([start])
    while True:
        minv = 100
        while not que.empty():
            p = que.get()
            if len(p) > minv:
                que.put(p)
                break
            if goal in p or goal in category.get(p[0], []):
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
