#!/bin/sh
FIREFOX_ROOT_DIR=~/firefox-52.0.2
BUILD_DIR=$FIREFOX_ROOT_DIR/obj-x86_64-pc-linux-gnu
FIREFOX_DIR=$BUILD_DIR/dist/bin/firefox
JS_DIR=$BUILD_DIR/js/src

curdir=`pwd`
clean_gcov () {
    cd $JS_DIR
    find . -name \*gcda -exec rm -f {} \;
}
make_gcov () {
    cd $JS_DIR
    find . -name \*gcda -exec gcov {} \;
}

crawl () {
    $FIREFOX_DIR --new-tab $1
}

clean_gcov
$curdir/keypress.py &
crawl $1
make_gcov
