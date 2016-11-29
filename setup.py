from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
import subprocess
import pathlib

pysvn_version_info = ('1', '9', '3')
_pysvn_soname = '_pysvn_3_5'

inno_exe = pathlib.Path('.', 'innoextract.exe').resolve()
pysvn_installer = pathlib.Path('.', 'py35-pysvn-svn194-1.9.3-1884-Win64.exe').resolve()


class BuildExtensions(build_ext):
    def build_extension(self, ext):
        if ext.name == _pysvn_soname:
            self._build_pysvn(ext)
        else:
            super(BuildExtensions, self).build_extension(ext)

    def _build_pysvn(self, ext):
        temp_dir = pathlib.Path(self.build_lib, 'temp')
        temp_dir.mkdir(parents=True, exist_ok=True)

        package_dir = pathlib.Path(self.build_lib, 'pysvn')

        result = subprocess.run([str(inno_exe), '-m', str(pysvn_installer)],
                                cwd=str(temp_dir), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                universal_newlines=True)

        pass


setup(
    name='pysvn',
    version='{}.{}.{}'.format(*pysvn_version_info),
    author="Barry Scott",
    author_email="barryscott@tigris.org",
    description="Subversion support for Python",
    url="http://pysvn.tigris.org",
    license="Apache Software License",
    keywords="subversion",
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'build_ext': BuildExtensions,
    },
    ext_modules=[
        Extension(
            _pysvn_soname, [])  # This used to tell setuptools that
                                # there is native extension, but
                                # they're not build using setuptools.
    ],
    classifiers=[
        'Topic :: Software Development :: Version Control'
    ],
)
