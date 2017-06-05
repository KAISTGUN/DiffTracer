DiffTracer
=========================
## Usage    

To use Our DiffTracer, ctags and diffutils should be upgraded.

Type below:
```bash
(sudo) ./install.sh
diff -v  # Diff version > 3.5 required.
```

Next, type below:
```bash
python Extractfunction.py [Unpatched Directory] [Patched Directory]

Example: python Extractfunction.py firefox-51.0 firefox-53.0
```

NOTE

This should produce 'answer__[unpatched directory]__[patched directory].csv' which includes the modified funtion's name.

Also, do not use abolute path. You should put 'firefox-' like folders in the first part of your path (refer to above Example).


## Corner Case
If File is deleted or renamed, DiffTrace does not work well; it can only diff if directory's paths are same.

##
./gen_gcov.sh: FIREFOX_ROOT_DIR
./check_cov.py: FIREFOX_DIR
