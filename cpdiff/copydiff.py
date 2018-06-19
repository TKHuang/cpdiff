import re
import os
import subprocess
import sys
import argparse

from pathlib import Path
from shutil import copy2

DEFAULT_ROOT_PATH = 'factory'


def get_args(args=None):
    parser = argparse.ArgumentParser(
        description='Copy files need to be update between commits.')
    # parser.add_argument('-p', '--preview', choices=['BTS', 'HTS', 'LITE', 'VIP'])
    parser.add_argument(
        '-p', '--preview', action='store_true', help='Preview mode.')
    parser.add_argument(
        '-s',
        '--start',
        default='HEAD~1',
        help='Start from commit(default:HEAD~1).')
    parser.add_argument(
        '-e', '--end', default='HEAD', help='End commit(default:HEAD).')
    parser.add_argument(
        '-o',
        '--out',
        required=True,
        help='Path the files should be copied to.')
    parser.add_argument(
        '-r',
        '--root',
        default=DEFAULT_ROOT_PATH,
        help=f'Path prefix to strip off(default:{DEFAULT_ROOT_PATH}).')
    args = parser.parse_args(args)
    return args


def git_diff(start, end):
    try:
        output = subprocess.check_output(
            f'git diff --name-only {start}..{end}', shell=True)
    except Exception as e:
        # print(f'error code: {e.returncode}')
        print(e)
        sys.exit(e.returncode)
    return output


def list_diff_files(start, end):
    diff_files = git_diff(start, end)

    # shell output is a binary string, should be convert to unicode str.
    try:
        diff_files = diff_files.decode('utf-8')
    except:
        diff_files = diff_files.decode('cp950')

    file_list = diff_files.split('\n')[:-1]
    file_list = [Path(file) for file in file_list]
    return file_list


def is_absolute_path(path):
    if getattr(path, 'as_posix', None) != None:
        isabs = path.as_posix().find('/') == 0 or path.is_absolute()
    else:
        isabs = path.find('/') == 0 or Path(path).is_absolute()
    return isabs


def strip_path_prefix(path, prefix):
    if is_absolute_path(path) or is_absolute_path(prefix):
        raise Exception(
            f'Error: relative path expected but given:\npath {path}\nprefix {prefix}'
        )
    try:
        return_val = path.relative_to(prefix)
    except ValueError:
        return_val = path
    return return_val


def gen_dst_path(filepath, outpath):
    outpath = Path(outpath)
    if is_absolute_path(filepath):
        raise Exception(
            f'Error: a relative path expected but given {filepath}.')
    elif not is_absolute_path(outpath):
        raise Exception(
            f'Error: an absolute outpath expected but given {outpath}.')
    return_path = outpath.joinpath(filepath)
    return return_path


def mkcopy(src, dst):
    if not dst.parent.exists():
        dst.parent.mkdir(parents=True)
    copy2(src, dst)


def main():
    args = get_args()
    src_files = list_diff_files(args.start, args.end)

    copy_files = [{'src': file} for file in src_files]
    # strip prefix (default is 'factory/').
    [
        file.update({
            'dst': strip_path_prefix(file['src'], args.root)
        }) for file in copy_files
    ]

    [
        file.update({
            'dst': gen_dst_path(file['dst'], args.out)
        }) for file in copy_files
    ]

    if args.preview == True:
        from pprint import pprint
        pprint(copy_files)
    else:
        [mkcopy(file['src'], file['dst']) for file in copy_files]


if __name__ == '__main__':
    main()