#!/usr/bin/env python3
from urllib.request import urlopen

import json
import os
import subprocess
import sys
import getpass


def get_json(url):
    return json.loads(urlopen(url).read().decode('utf-8'))


def download_file(src_url, dest_path):
    print(dest_path)
    subprocess.call(
        ['curl', '-L', '-#', '-o', dest_path, src_url])


def download_github_artifacts():
    release = get_json(
        'https://api.github.com/repos/xattr/xattr/releases/latest')
    for asset in release['assets']:
        download_file(asset['browser_download_url'], 'dist/{name}'.format(**asset))


def get_version():
    return subprocess.check_output(
        [sys.executable, 'setup.py', '--version'],
        encoding='utf8'
    ).strip()


def artifact_matcher(version):
    prefix = 'xattr-{}'.format(version)
    def matches(fn):
        return (
            fn.startswith(prefix) and
            os.path.splitext(fn)[1] in ('.exe', '.whl') and
            not fn.endswith('-none-any.whl')
        ) or fn == '{}.tar.gz'.format(prefix)
    return matches


def upload_artifacts(version):
    artifacts = set(os.listdir('dist'))
    matches = artifact_matcher(version)
    args = ['twine', 'upload']
    for fn in filter(matches, artifacts):
        args.append(os.path.join('dist', fn))
    subprocess.check_call(args)


def main():
    try:
        os.makedirs('dist')
    except OSError:
        pass
    download_github_artifacts()
    version = get_version()
    upload_artifacts(version)


if __name__ == '__main__':
    main()
