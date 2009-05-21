import pyloc.python_source
import pyloc.cpp_source

lang_map = {
    '*.py' : ('Python', pyloc.python_source.loc),
    '*.cpp' : ('C++', pyloc.cpp_source.loc)
    }
