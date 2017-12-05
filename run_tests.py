import os
import subprocess
import sys


def do_call(args):
    oneline = ['"{}"'.format(x) for x in args]
    oneline = ' '.join(oneline)
    print('[{}]> {}'.format(os.getcwd(), oneline))
    try:
        subprocess.check_call(args, env=os.environ)
    except subprocess.CalledProcessError as error:
        print(error)
        print(error.output)
        sys.exit(1)


def run_flake8():
    print('Run flake8')
    do_call(['flake8', '.'])


def run_python_tests():
    print('Run python tests')
    do_call([
        'sh', '-c',
        'python -m unittest',
    ])


def main():
    run_flake8()
    run_python_tests()


if __name__ == "__main__":
    main()
