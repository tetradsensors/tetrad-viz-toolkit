import io
from setuptools import setup


def read_files(files):
    data = []
    for file in files:
        with io.open(file, encoding='utf-8') as f:
            data.append(f.read())
    return "\n".join(data)


long_description = read_files(['README.md', 'CHANGELOG.md'])

meta = {}
with io.open('./viz-toolkit/version.py', encoding='utf-8') as f:
    exec(f.read(), meta)

setup(
    name="viz-toolkit",
    description="Toolkit for visualizations using Tetrad infrastructure.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=meta['__version__'],
    author="Saurabh Kumar",
    author_email="me+github@saurabh-kumar.com",
    url="https://github.com/theskumar/python-dotenv",
    keywords=['environment variables', 'deployments', 'settings', 'env', 'dotenv',
              'configurations', 'python'],
    packages=['dotenv'],
    package_dir={'': 'src'},
    package_data={
        'dotenv': ['py.typed'],
    },
    python_requires=">=3.5",
    extras_require={
        'cli': ['click>=5.0', ],
    },
    entry_points='''
        [console_scripts]
        dotenv=dotenv.cli:cli
    ''',
    license='BSD-3-Clause',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Environment :: Web Environment',
    ]
)