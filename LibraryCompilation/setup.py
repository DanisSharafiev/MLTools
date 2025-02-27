from setuptools import setup, Extension
import pybind11

module = Extension(
    'MLInnoTools',
    sources=['MLInnoTools.cpp'],
    include_dirs=[pybind11.get_include()],
    extra_compile_args=["/std:c++17", "/O2"],
    language='c++',
)

setup(
    name='MLInnoTools',
    ext_modules=[module],
)
