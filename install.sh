apt-get install ctags
wget https://ftp.gnu.org/gnu/diffutils/diffutils-3.6.tar.xz
xz -d diffutils-3.6.tar.xz
tar -xUf diffutils-3.6.tar
cd diffutils-3.6
./configure && make && make install
cd ..
rm -rf diffutils-3.6.tar
rm -rf diffutils-3.6.tar.xz
rm -rf diffutils-3.6
