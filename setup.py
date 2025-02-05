from setuptools import setup, Extension
import pybind11

module = Extension(
    'MLInnoTools',
    sources=['MLInnoTools.cpp'],
    include_dirs=[pybind11.get_include()],
    language='c++',
)

setup(
    name='MLInnoTools',
    ext_modules=[module],
)
