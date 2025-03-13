from setuptools import setup, Extension
import pybind11

module = Extension(
    'MLTools',
    sources=['MLTools.cpp'],
    include_dirs=[pybind11.get_include()],
    extra_compile_args=["/std:c++17", "/O2"],
    language='c++',
)

setup(
    name='MLTools',
    ext_modules=[module],
)
