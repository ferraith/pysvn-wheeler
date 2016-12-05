pysvn-wheeler
=============

|Build Status| |Latest Release|

Wheel packages for `pysvn <http://pysvn.tigris.org/>`__.

This is a setup script to build wheel packages for ``pysvn``. The author of ``pysvn`` provides only setup files for Windows which makes it difficult to use ``pysvn`` in modern Python environments like a virtual environment. The de-facto standard for Python packages is the ``wheel`` format which gives you for instance the possibility to manage your packages with pip.

``pysvn-wheeler`` extracts the ``pysvn`` setup file and creates a platform-specific wheel package out of it. It doesn't compile ``Subversion``, its dependencies and ``pysvn`` from source. Because of that the content of a wheel and the corresponding setup file is equal.

Installation
------------

``pysvn-wheeler`` can be used to install ``pysvn`` with pip using an on-demand created wheel package. Additionally wheel packages for all common Python versions are provided at the `release <https://github.com/ferraith/pysvn-wheeler/releases>`__ page.

From Source Code
****************

::

    > git clone https://github.com/ferraith/pysvn-wheeler.git
    > cd pysvn-wheeler
    > mkdir pysvn
    > wget -P pysvn <pysvn_download_link>
    > pip install .

From GitHub Releases
********************

::

    > pip install <pysvn_wheel>

.. |Build Status| image:: https://ci.appveyor.com/api/projects/status/github/ferraith/pysvn-wheeler?branch=master&svg=true
   :target: https://ci.appveyor.com/project/ferraith/pysvn-wheeler/branch/master
   :alt: Build Status

.. |Latest Release| image:: https://img.shields.io/github/release/ferraith/pysvn-wheeler.svg
   :target: https://github.com/ferraith/pysvn-wheeler/releases
   :alt: Latest Release
