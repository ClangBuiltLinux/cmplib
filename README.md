# cmplibc

Tooling to analyzing binaries to better understand what symbols are expected
to be provided from what libary at runtime.

## Checking what symbols are provided by a library

`./provides libfoo.[a,so]`

## Checking what symbols an executable depends on

`./depends.py a.out`

## Checking compatibility between lib1 and lib2

`./check_compat.py a.out lib1.[a,so] lib2.[a,so]`

# License

Copyright 2023 Google LLC

Licensed under Apache 2.0
