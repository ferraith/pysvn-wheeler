import distutils.log
import distutils.version
import distutils.errors
import pathlib
import re
import shutil
import subprocess

import setuptools
import setuptools.command.build_ext as _build_ext


# TODO: Add inline docu
class InnoSetupExtension(setuptools.Extension):
    def __init__(self, name, sources, version=None, inno_setup=None, *args, **kw):
        self.version = version
        self.inno_setup = inno_setup

        setuptools.Extension.__init__(self, name, sources, *args, **kw)


class build_ext(_build_ext.build_ext):
    INNOUNP_EXE = pathlib.Path('tools/innounp.exe')

    def build_extension(self, ext):
        if isinstance(ext, InnoSetupExtension):
            self.extract_inno_setup(ext)
        else:
            super(build_ext, self).build_extension(ext)

    def extract_inno_setup(self, ext):
        if not ext.inno_setup.is_file():
            raise distutils.errors.DistutilsFileError('Passed setup path isn\'t valid.')

        package_dir = pathlib.Path(self.build_lib, 'pysvn')
        package_dir.mkdir(parents=True, exist_ok=True)

        try:
            # clean up package directory
            shutil.rmtree(str(package_dir))
            # extract setup file to package directory
            subprocess.run([str(self.INNOUNP_EXE), '-x', '-c{app}', '-d' + str(package_dir),
                            str(ext.inno_setup)], check=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            raise distutils.errors.DistutilsExecError('Setup file couldn\'t be extracted.\n'
                                                      '{}'.format(e.stdout))

if __name__ == '__main__':
    # search for pysvn setup file
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
