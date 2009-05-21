import pyloc.python_source
import pyloc.cpp_source

lang_map = {
    '*.py' : ('python_source', pyloc.python_source.loc),
    '*.cpp' : ('cpp_source', pyloc.cpp_source.loc)
    }
