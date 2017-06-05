#!/usr/bin/env python
import os
import subprocess
import sys
import re

FIREFOX_DIR = '/home/yum3/firefox-52.0.2/'
BUILD_DIR = 'obj-x86_64-pc-linux-gnu/'
gcov_files = 0

def get_gcov_list():
    global gcov_files
    cmd = r"find %s -name \*gcov" % (FIREFOX_DIR + BUILD_DIR)
    gcov_files = subprocess.check_output(cmd, shell=True).rstrip().split('\n')

def get_called_times(src, lineno):
    #cmd = 'egrep "^function" %s/*gcov|cut -f2,3 -d","|c++filt' \
    #      '|egrep "::%s[\(|\<]"' \
    #      % (FIREFOX_DIR + BUILD_DIR + "js/src")
    #gcov_funcs = subprocess.check_output(cmd, shell=True).rstrip().split('\n')
    cnt = 0

    cmd = 'egrep "Source:.*%s$" %s -rl' % (src, ' '.join(gcov_files))

    # must be UNIQUE
    try:
        gcov_file = subprocess.check_output(cmd, shell=True).rstrip().split('\n')[0]
    except:
        # does not exist
        return -1
    t = re.search("\n\s*(\d+|-|#{5}|={4}):\s*%d:"%lineno, open(gcov_file).read())
    cnt = t.group(1)
    print(t.group(0))
    if cnt == '#'*5 or cnt == '='*4 or cnt == '-':
        return 0
    else:
        return int(cnt)

def main():
    f = open("top-1m.csv", "rt")
    for line in f:
        # fetch one url
        cnt, url = line.rstrip().split(",")

        cnt = int(cnt)
        if cnt > int(sys.argv[1]): sys.exit(0)

        # generate gcov
        #os.system("./gen_gcov.sh %s" % url)
        get_gcov_list()

        # get function list from diff result
        ans_fp = open("answer.txt", "rt")

        # get function list from gcov
        for l in ans_fp:
            print(l)
            file_loc, lines = l.rstrip().split("\t")
            lines = lines.split(",")

            #f_index = file_loc.index("/") # keep where to change

            #file_loc = FIREFOX_DIR + file_loc[f_index+1:]
            #if not os.path.exists(FIREFOX_DIR + file_loc):
            #    print("File %s does not exist." % file_loc)
            #    continue

            for lineno in lines:
                times = get_called_times(file_loc, int(lineno))
                if times > 0:
                    print("%s:%s executed %d times." % (file_loc, 'asdf',
                      times))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # we can't test all 1-million sites
        print("Usage: %s %s" % (sys.argv[0], "<how_many_sites>"))
        sys.exit(1)
    main()
