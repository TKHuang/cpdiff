# Copy your fresh codes to anywhere in a handy way!
## How it works?
copydiff use git diff to find out those files you modified, then copy these files to anywhere you want!

## How to use?

Install

`python setup.py install`

```shell
$ cpdiff -h
usage: __main__.py [-h] [-p] [-s START] [-e END] -o OUT [-r ROOT]

Copy files need to be update between commits.

optional arguments:
  -h, --help            show this help message and exit
  -p, --preview         Preview mode.
  -s START, --start START
                        Start from commit(default:HEAD~1).
  -e END, --end END     End commit(default:HEAD).
  -o OUT, --out OUT     Path the files should be copied to.
  -r ROOT, --root ROOT  Path prefix to strip off(default:factory).
```

- By default copydiff compares last one commit to filter files.

        $ cpdiff -o 'C:\yourpath'

        equals

        $ cpdiff -s HEAD~1 -e HEAD -o 'C:\yourpath'

        or use commit sha1

        $ cpdiff -s {commit-sha1} -e HEAD -o 'C:\yourpath'

- Compare to last 6 commit.

        $ cpdiff -o 'C:\yourpath' --start HEAD~6

- Preview what will be copied.

        $ cpdiff -o 'C:\yourpath' --start HEAD~6 --preview

        [{'dst': WindowsPath('C:/yourpath/commit3'), 'src': WindowsPath('commit3')},
        {'dst': WindowsPath('C:/yourpath/gg/22222'), 'src': WindowsPath('gg/22222')},
        {'dst': WindowsPath('C:/yourpath/master'), 'src': WindowsPath('master')},
        {'dst': WindowsPath('C:/yourpath/nofastmerge'),
        'src': WindowsPath('nofastmerge')}]

## Caution
The output path(-o) needs an absolute path and should be wrapped by quotes when on windows.