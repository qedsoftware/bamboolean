import urllib.request

from run_tests import do_call
from conf import PACKAGE_NAME, VERSION


def upload():
    print('Uploading package...')
    do_call(['python', 'setup.py', 'sdist'])
    do_call(['python', 'setup.py', 'bdist_wheel'])
    do_call(['twine', 'upload', 'dist/*'])


def version_exists():
    url = ("https://pypi.python.org/pypi"
           "?:action=display&name={package_name}&version={version}".format(
               package_name=PACKAGE_NAME,
               version=VERSION))
    try:
        req = urllib.request.Request(url, method="HEAD")
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise e
    return True


def main():
    if version_exists():
        print('Please bump your version. Version {} already exists'.format(
            VERSION))
    else:
        upload()


if __name__ == '__main__':
    main()
