import distutils.log
import distutils.version
import distutils.errors
import sys
import re
import subprocess

import setuptools
import setuptools.command.build_ext as _build_ext

if sys.version_info < (3, 4):
    import pathlib2 as pathlib
else:
    import pathlib


class InnoSetupExtension(setuptools.Extension):
    """Extension that consists of an Inno Setup file"""
    def __init__(self, name, sources, version=None, inno_setup=None, *args, **kw):
        """Initializes a new InnoSetupExtension object.

        :param version: version of setup file
        :param inno_setup: path to setup file
        """
        self.version = version
        self.inno_setup = inno_setup

        setuptools.Extension.__init__(self, name, sources, *args, **kw)


class build_ext(_build_ext.build_ext):
    """A specialization of the setuptools command 'build_ext' for processing Inno Setup files.

    :cvar _INNOUNP_EXE: path to innounp tool
    """
    _INNOUNP_EXE = pathlib.Path('tools/innounp.exe')

    def build_extension(self, ext):
        """Builds an extension part of the python package."""
        if isinstance(ext, InnoSetupExtension):
            self.extract_inno_setup(ext)
        else:
            super(build_ext, self).build_extension(ext)

    def extract_inno_setup(self, ext):
        """Extracts app folder of Inno Setup file to corresponding package directory."""
        if not ext.inno_setup.is_file():
            raise distutils.errors.DistutilsFileError('Passed setup path isn\'t valid.')

        package_dir = pathlib.Path(self.build_lib, ext.name)

        try:
            # extract setup file to package directory
            subprocess.check_output([str(self._INNOUNP_EXE), '-x', '-y', '-c{app}', '-d' +
                                     str(package_dir), str(ext.inno_setup)],
                                    stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            raise distutils.errors.DistutilsExecError('Setup file couldn\'t be extracted.\n'
                                                      '{}'.format(e.stdout))


if __name__ == '__main__':
    # search for setup file in pysvn folder
    pysvn_inno_setup = None
    pysvn_regex = re.compile('py\d{2}-pysvn-svn\d{3,4}-((?:\d+.){2}\d+)-\d{4}.*.exe$')
    for pysvn_exe in pathlib.Path('pysvn').iterdir():
        match = pysvn_regex.search(pysvn_exe.name)
        if match and pysvn_exe.is_file():
            # first match will be used
            pysvn_inno_setup = InnoSetupExtension(
                'pysvn', [], version=distutils.version.StrictVersion(match.group(1)),
                inno_setup=pysvn_exe)
            break

    if not pysvn_inno_setup:
        raise distutils.errors.DistutilsFileError('No pysvn setup file found.')

    setuptools.setup(
        name='pysvn',
        version=str(pysvn_inno_setup.version),
        author="Barry Scott",
        author_email="barryscott@tigris.org",
        description="Subversion support for Python",
        long_description="The pysvn module is a python interface to the Subversion version control "
                         "system. It depends on the native Apache Subversion client which is part "
                         "of this package. Additionally on Windows platform a VC++ Redistributable "
                         "suitable for your Python version have to be installed.",
        platforms=['win32'],
        url="http://pysvn.tigris.org",
        license="Apache Software License",
        keywords="subversion",
        zip_safe=False,
        cmdclass={'build_ext': build_ext},
        ext_modules=[pysvn_inno_setup],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Software Development :: Version Control',
            'Environment :: Win32 (MS Windows)',
            'Operating System :: Microsoft :: Windows'
        ],
    )
