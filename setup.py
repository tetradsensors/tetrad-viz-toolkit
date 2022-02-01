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
with io.open('./tetrad-viz-toolkit/version.py', encoding='utf-8') as f:
    exec(f.read(), meta)

setup(
    name="tetrad-viz-toolkit",
    description="Toolkit for visualizations using Tetrad infrastructure.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=meta['__version__'],
    author="Tom Becnel",
    author_email="thomas.becnel@tetradsensors.com",
    url="https://github.com/tetradsensors/tetrad-viz-toolkit",
    keywords=['environment variables', 'deployments', 'settings', 'env', 'dotenv',
              'configurations', 'python'],
    packages=['tetrad-viz-toolkit'],
    package_dir={'': 'tetrad-viz-toolkit'},
    package_data={
        'tetrad-viz-toolkit': ['py.typed'],
    },
    python_requires=">=3.5",
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