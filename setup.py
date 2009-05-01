from setuptools import setup, find_packages
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


    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # install_requires = ['docutils>=0.3'],

    #package_data = {
    #    # If any package contains *.txt or *.rst files, include them:
    #    '': ['*.txt', '*.rst'],
    #    # And include any *.msg files found in the 'hello' package, too:
    #    'hello': ['*.msg'],
    #}

    # metadata for upload to PyPI
    author = "Austin Bingham",
    author_email = "austin.bingham@gmail.com",
    description = "A simply lines-of-code counter for python",
    license = "MIT",
    keywords = "python loc sloc lines-of-code",
    # url = "http://example.com/HelloWorld/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
