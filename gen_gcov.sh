#!/bin/sh
FIREFOX_ROOT_DIR=~/firefox-52.0.2
BUILD_DIR=$FIREFOX_ROOT_DIR/obj-x86_64-pc-linux-gnu
FIREFOX_DIR=$BUILD_DIR/dist/bin/firefox
JS_DIR=$BUILD_DIR/js/src

make_gcov () {
    cd $JS_DIR

    for file in $(find . -name \*gcda); do
        #file=$(realpath --relative-to="$FIREFOX_ROOT_DIR/obj-x86_64-pc-linux-gnu" $file)
        echo "Processing ${file}..."
        gcov -i $file > /dev/null
    done
}

crawl () {
    timeout 60 $FIREFOX_DIR --new-instance --new-tab $1
}

crawl $1
make_gcov