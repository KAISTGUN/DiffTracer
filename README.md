DiffTracer
=========================
## Usage    

For extracting all of funtion, you should make tags file.

Type below:
```bash
(sudo) apt get install ctags

ctags -R -x --c++-kinds=+p --fields=iaSnt --languages=c++ --exclude=*.h [Unpatched Directory Name]  | grep function > tags
 
Example: ctags -R -x --c++-kinds=+p --fields=iaSnt --languages=c++ --exclude=*.h firefox-51.0/  | grep function > tags
```

It will makes 'tags' file. then you are good to go.

Next, type below:
```bash
python Extractfunction.py [Unpatched Directory] [Patched Directory]

Example: python Extractfunction.py firefox-51.0/ firefox-53.0/
```

You should put '/' characters to the last of your directory name.

This should produce 'answer.txt' which includes the modified funtion's name.


## Corner Case
If File is deleted or renamed, this does not work well; it can only diff if path + filename is same.
