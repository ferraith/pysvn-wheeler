import distutils.log
import distutils.version
import subprocess
import pathlib

import setuptools
import setuptools.command.build_ext as _build_ext


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
            distutils.log.fatal('Passed Inno Setup path isn\'t valid.')

        package_dir = pathlib.Path(self.build_lib, 'pysvn')
        package_dir.mkdir(parents=True, exist_ok=True)

        result = subprocess.run([str(self.INNOUNP_EXE), '-x', '-c{app}', '-d' + str(package_dir),
                                 str(ext.inno_setup)], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, universal_newlines=True)

        # TODO: Check return code and print error part of result
        # TODO: Add a install hint regarding VS-Redistributable


pysvn_inno_setup = InnoSetupExtension(
    'pysvn', [], version=distutils.version.StrictVersion('1.9.3'),
    inno_setup=pathlib.Path('pysvn/py35-pysvn-svn194-1.9.3-1884-Win64.exe'))


setuptools.setup(
    name='pysvn',
    version=str(pysvn_inno_setup.version),
    author="Barry Scott",
    author_email="barryscott@tigris.org",
    description="Subversion support for Python",
    url="http://pysvn.tigris.org",
    license="Apache Software License",
    keywords="subversion",
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'build_ext': build_ext,
    },
    ext_modules=[
        pysvn_inno_setup
    ],
    classifiers=[
        'Topic :: Software Development :: Version Control'
    ],
)
