DiffTracer
=========================
## Usage    

To use Our DiffTracer, ctags and diffutils should be upgraded.

Type below:
```bash
(sudo) ./install.sh
diff -v  # Check Diff version
```

Next, type below:
```bash a
python Extractfunction.py [Unpatched Directory] [Patched Directory]

Example: python Extractfunction.py firefox-51.0/ firefox-53.0/
```

NOTE : You should put '/' characters to the last of your directory name.

This should produce 'answer.txt' which includes the modified funtion's name.

Also, do not use abolute path. You should put 'firefox-' like folders in the first part of your path (refer to above Example).


## Corner Case
If File is deleted or renamed, this does not work well; it can only diff if path + filename is same.
