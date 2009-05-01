from setuptools import setup, find_packages

long_description = '''pyloc scans a list of directory trees for python source files,
counting lines of code. For each tree, two counts are reported:

 * A line count include comments and blank lines
 * A line count with out comments and blank lines

Finally, sums of both counts are reported.'''

setup(
    name = "pyloc",
    version = "0.9",
    package_dir = {'':'src'},
    packages = find_packages('src'),

    entry_points = {
        'console_scripts': [
            'pyloc = pyloc.pyloc:main'
        ]
    },

    # metadata for upload to PyPI
    author = "Austin Bingham",
    author_email = "austin.bingham@gmail.com",
    description = "A lines-of-code counter for python",
    license = "MIT",
    keywords = "python loc sloc lines-of-code",
    long_description=long_description,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development'],

    install_requires=['setuptools']

    )
