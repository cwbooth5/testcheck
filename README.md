## Synopsis

This is intended to be used as a code quality checker. It can be run prior to
code review and/or check-in.

## Code Example

Example: run all checks in verbose mode
```
prompt$ ./checker.py checker.py -av
[ Spellcheck ]  [DONE]
[ Cyclomatic Complexity ]
checker.py
    F 27:0 edits1 - C
    F 137:0 main - B
    M 82:4 CodeChecker.check_spelling - B
    F 50:0 add_term - B

[ Raw Metrics ]
checker.py
    LOC: 169
    LLOC: 125
    SLOC: 136
    Comments: 8
    Multi: 8
    Blank: 33
    - Comment Stats
        (C % L): 5%
        (C % S): 6%
        (C + M % L): 9%

No config file found, using default configuration
************* Module checker
C:159, 0: Line too long (81/80) (line-too-long)
C:161, 0: Line too long (81/80) (line-too-long)
C:162, 0: Line too long (81/80) (line-too-long)
C:164, 0: Line too long (81/80) (line-too-long)
C:165, 0: Line too long (82/80) (line-too-long)
C: 12, 0: Missing function docstring (missing-docstring)
C: 16, 0: Missing function docstring (missing-docstring)
C: 18, 8: Invalid variable name "f" (invalid-name)
W: 23,21: Used builtin function 'file' (bad-builtin)
C: 24, 0: Invalid constant name "alphabet" (invalid-name)
C: 27, 0: Missing function docstring (missing-docstring)
C: 28, 4: Invalid variable name "s" (invalid-name)
C: 36, 0: Missing function docstring (missing-docstring)
W: 40,10: Redefining name 'words' from outer scope (line 12) (redefined-outer-name)
C: 40, 0: Missing function docstring (missing-docstring)
C: 44, 0: Missing function docstring (missing-docstring)
W:137, 9: Redefining name 'parser' from outer scope (line 157) (redefined-outer-name)
C:157, 4: Invalid constant name "parser" (invalid-name)
[ pylint ] Your code has been rated at 8.36/10
prompt$
```

## Motivation

This exists because I need a consistent way to review code prior to check in. This will improve the code coming into the review stage as well as assist in improving the quality of existing code.

## Installation

You will need to install some things using *pip*. The package *flake8* contains pip and pylint. If you already have pylint and pep8, you can skip this step.
```
pip install flake8
```

## Contributors

Bill Booth
