import pytest
from functools import partial
from cpdiff import copydiff as cp


def test_get_args():
    testfn = cp.get_args
    test_set = [{
        'in': ['-p', '-o', 'testpath'],
        'out': {
            'start': 'HEAD~1',
            'end': 'HEAD',
            'out': 'testpath',
            'preview': True,
            'root': 'factory'
        },
        'description': ''
    }, {
        'in': [
            '-s', 'HEAD~6', '-e', 'HEAD~2', '-o', 'testpath123', '-r',
            'anotherpath/GG'
        ],
        'out': {
            'start': 'HEAD~6',
            'end': 'HEAD~2',
            'out': 'testpath123',
            'preview': False,
            'root': 'anotherpath/GG'
        },
        'description':
        ''
    }]

    def assertfn(result, target):
        assert result.__dict__ == target

    runcase(testfn, test_set, assertfn)


def test_list_diff_files(monkeypatch):
    from pathlib import Path
    testfn = cp.list_diff_files
    test_set = [{
        'in': ('HEAD~2', 'HEAD'),
        'out': [Path('master'), Path('nofastmerge')],
        'mock': [(cp, 'git_diff', lambda x, y: b'master\nnofastmerge\n')]
    }, {
        'in': ('HEAD~6', 'HEAD'),
        'out': [Path('commit3'), Path('gg/22222'), Path('master'), Path('nofastmerge')],
        'mock': [(cp, 'git_diff',
                  lambda x, y: b'commit3\ngg/22222\nmaster\nnofastmerge\n')]
    }]

    with monkeypatch.context() as m:
        runcase(testfn, test_set, mock=m)


def test_strip_path_prefix():
    from pathlib import Path
    testfn = cp.strip_path_prefix
    test_set = [{
        'in': (Path('factory/123456.xyz'), 'factory'),
        'out': Path('123456.xyz')
    }, {
        'in': (Path('factory/inner/123456.xyz'), 'factory'),
        'out': Path('inner/123456.xyz')
    }, {
        'in': (Path('/factory/21355.xxx'), 'factory'),
        'error': Exception,
        'description': 'input path should be a relative path.'
    }, {
        'in': (Path('apath/1289378934.xyyyydfs'), '/apath'),
        'error': Exception,
        'description': 'input prefix should be a relative path.'
    }]

    runcase(testfn, test_set)


def test_is_absolute_path():
    from pathlib import Path
    testfn = cp.is_absolute_path
    test_set = [{
        'in': Path('/path/from/root'),
        'out': True
    }, {
        'in': Path('relative/path'),
        'out': False
    }, {
        'in': '/path/from/root',
        'out': True
    }, {
        'in': 'relative/path',
        'out': False
    }, {
        'in': 123,
        'error': AttributeError
    }, {
        'in': Path(r'C:\Users\011321\Desktop\gittest\tests'),
        'out': True
    }]
    runcase(testfn, test_set)


def test_gen_dst_path():
    from pathlib import Path
    testfn = cp.gen_dst_path
    test_set = [{
        'in': (Path('folder1/test.py'), '/root/output/path'),
        'out': Path('/root/output/path/folder1/test.py')
    }, {
        'in': (Path('folder1/subfolder/test.py'), '/root/output/path'),
        'out':
        Path('/root/output/path/folder1/subfolder/test.py')
    }, {
        'in': ('/folder1/subfolder/test.py', '/root/output/path'),
        'out': Path('/root/output/path/folder1/subfolder/test.py'),
        'description': 'filepath should be a relative path.',
        'error': Exception
    }, {
        'in': ('folder1/subfolder/test.py', 'root/output/path'),
        'out': Path('/root/output/path/folder1/subfolder/test.py'),
        'description': 'outpath should be an absolute path.',
        'error': Exception
    }]
    runcase(testfn, test_set)


def runcase(testfn, test_set, assertfn=None, mock=None):
    def runtest(testfn, test, assertfn=None):
        # list input should be directly feed in.
        if type(test['in']) == tuple:
            fn = partial(testfn, *test['in'])
        else:
            fn = partial(testfn, test['in'])
        if test.get('error') is not None:
            # fail test.
            with pytest.raises(test['error']) as exc_info:
                fn()
            assert exc_info.type == test['error']
        else:
            # success test.
            result = fn()
            if assertfn is None:
                assert result == test['out']
            else:
                assertfn(result, test['out'])

    for test in test_set:
        # mocking
        if test.get('mock') is None:
            runtest(testfn, test, assertfn)
        elif len(test['mock']) > 0:
            for mocksetting in test['mock']:
                mock.setattr(*mocksetting)
            runtest(testfn, test, assertfn)


if __name__ == "__main__":
    pytest.main()