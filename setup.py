import distutils.log
import subprocess
import pathlib

import setuptools.command.build_ext

# TODO: Extract version out of file or filename
pysvn_version_info = ('1', '9', '3')
# TODO: pass file name?
pysvn_inno_setup = 'py35-pysvn-svn194-1.9.3-1884-Win64.exe'


class build_ext(setuptools.command.build_ext.build_ext):
    INNOUNP_EXE = pathlib.Path('tools', 'innounp.exe')

    def build_extension(self, ext):
        if ext.name == pysvn_inno_setup:
            self.extract_inno_setup(ext)
        else:
            super(build_ext, self).build_extension(ext)

    def extract_inno_setup(self, ext):
        inno_setup_path = pathlib.Path(ext.name)
        if not inno_setup_path.is_file():
            distutils.log.fatal('Passed Inno Setup path isn\'t valid.')

        package_dir = pathlib.Path(self.build_lib, 'pysvn')
        package_dir.mkdir(parents=True, exist_ok=True)

        result = subprocess.run([str(self.INNOUNP_EXE), '-x', '-c{app}', '-d' + str(package_dir),
                                 str(inno_setup_path)], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, universal_newlines=True)

        # TODO: Check return code and print error part of result
        # TODO: Maybe add a install hint regarding VS-Redistributable


setuptools.setup(
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
        'build_ext': build_ext,
    },
    ext_modules=[
        setuptools.Extension(
            pysvn_inno_setup, [])  # This used to tell setuptools that
                                   # there is native extension, but
                                   # they're not build using setuptools.
    ],
    classifiers=[
        'Topic :: Software Development :: Version Control'
    ],
)
