import pyloc.python_source
import pyloc.cpp_source

lang_map = {
    '*.py'  : ('Python', pyloc.python_source.loc),
    '*.cpp' : ('C++', pyloc.cpp_source.loc),
    '*.h'   : ('C/C++ Header', pyloc.cpp_source.loc),
    '*.hpp'   : ('C++ Header', pyloc.cpp_source.loc),
    }
