import os

if __name__ == '__main__':
    ver_fn = 'viztools/version.py'
    with open(ver_fn, 'r') as f:
        line = f.read()

    version = line.split('"')[1]
    major, minor, micro = version.split('.')
    new_version = f'__version__ = "{major}.{int(minor) + 1}.0"\n'

    with open(ver_fn, 'w') as f:
        f.write(new_version)

    os.system('python setup.py bdist_egg && pip install .')
