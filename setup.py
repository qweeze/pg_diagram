import pathlib
from setuptools import setup


setup(
    name='pg-diagram',
    author='qweeze',
    author_email='qweeeze@gmail.com',
    version='0.1.0',
    description='A tool for creating ER diagrams from postgresql database schemas',
    long_description=(pathlib.Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/qweeze/pg_diagram',
    packages=['pg_diagram'],
    install_requires=[
        'sqlparse',
        'graphviz',
        'click',
    ],
    entry_points={
        'console_scripts': ['pg_diagram=pg_diagram.__main__:main'],
    },
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
