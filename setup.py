import io
from setuptools import find_packages, setup


def read_files(files):
    data = []
    for file in files:
        with io.open(file, encoding='utf-8') as f:
            data.append(f.read())
    return "\n".join(data)


long_description = read_files(['README.md', 'CHANGELOG.md'])

meta = {}
with io.open('./viztools/version.py', encoding='utf-8') as f:
    exec(f.read(), meta)

setup(
    name="Tetrad Visualization Toolkit",
    description="Toolkit for visualizations using Tetrad infrastructure.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=meta['__version__'],
    author="Tom Becnel",
    author_email="thomas.becnel@tetradsensors.com",
    url="https://github.com/tetradsensors/tetrad-viz-toolkit",
    packages=find_packages(exclude=["*test*"]),
    python_requires=">=3.5",
    license='MIT',
)