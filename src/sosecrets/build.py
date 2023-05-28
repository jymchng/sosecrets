import os
# https://stackoverflow.com/questions/63679315/how-to-use-cython-with-poetry
def get_ext_paths(root_dir, exclude_files):
    """get filepaths for compilation"""
    paths = []

    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if os.path.splitext(filename)[1] not in  ['.py', '.pyi', '.pyx']:
                continue

            file_path = os.path.join(root, filename)
            if file_path in exclude_files:
                continue

            paths.append(file_path)
    print("Paths: ", paths)
    return paths

import sosecrets

ROOT_DIR = sosecrets.__file__

# See if Cython is installed
try:
    from Cython.Build import cythonize
# Do nothing if Cython is not available
except ImportError:
    # Got to provide this function. Otherwise, poetry will fail
    def build(setup_kwargs: dict):
        pass
# Cython is installed. Compile
else:
    print("Cython is installed")
    from setuptools import Extension
    from setuptools.dist import Distribution
    from distutils.command.build_ext import build_ext

    # This function will be executed in setup.py:
    def build(setup_kwargs: dict):
        # The file you want to compile
        extensions = get_ext_paths(ROOT_DIR)

        # gcc arguments hack: enable optimizations
        os.environ['CFLAGS'] = '-O3'

        # Build
        setup_kwargs.update({
            'ext_modules': cythonize(
                extensions,
                language_level=3,
                compiler_directives={'linetrace': True},
            ),
            'cmdclass': {'build_ext': build_ext}
        })