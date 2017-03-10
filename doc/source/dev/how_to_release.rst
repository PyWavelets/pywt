Guidelines for Releasing PyWavelets
===================================

The following are guidelines for preparing a release of PyWavelets.  The
notation ``vX.X.X`` in the commands below would be replaced by the actual release
number.


Updating the release notes
--------------------------

Prior to the release, make sure the release notes are up to date.  The author
lists can be generated via::

    python  ./util/authors.py vP.P.P..

where ``vP.P.P`` is the previous release number.

The lists of issues closed and PRs merged can be generated via
(script requires Python 2.X to run)::

    python ./util/gh_lists.py vX.X.X


Tag the release
---------------

Change ``ISRELEASED`` to ``True`` in ``setup.py`` and commit.

Tag the release via::

    git tag -s vX.X.X

Then push the ``vX.X.X`` tag to the PyWavelets GitHub repo.

Note that while Appveyor will build wheels for Windows, it is preferred to
get those wheels from the step below.  Instructions for grabbing Appveyor
wheels manually here for reference only: if the commit with
``ISRELEASED=True`` is submitted as a PR, the wheels can be downloaded from
Appveyor once it has run on the PR.  They can be found under the "Artifacts"
tab in the Appveyor interface.


Build Windows, OS X and Linux wheels and upload to PyPI
-------------------------------------------------------

Push a commit with the new tag and updates of dependency versions where needed
to https://github.com/MacPython/pywavelets-wheels.  The wheels will be
produced automatically and uploaded to http://wheels.scipy.org/.
From there they can be uploaded to
`PyPI <https://pypi.python.org/pypi/PyWavelets>`_ automatically with
``wheel-uploader``.

See the README on https://github.com/MacPython/pywavelets-wheels for more
details.

Create the source distribution
------------------------------

Remove untracked files and directories with ``git clean``.
*Warning: this will delete files & directories that are not under version
control so you may want to do a dry run first by adding -n, so you can see what
will be removed*::

    git clean -xfdn

Then run without ``-n``::

    git clean -xfd

Create the source distribution files via::

    python setup.py sdist --formats=gztar,zip


Upload the release to PyPI
--------------------------

The binary Windows wheels downloaded from Appveyor (see above) should
also be placed into the ``/dist`` subfolder along with the sdist archives.

The wheels and source distributions created above can all be securely uploaded
to pypi.python.org using twine::

    twine upload -s dist/*

Note that the documentation on ReadTheDocs (http://pywavelets.readthedocs.org)
will have been automatically generated, so no actions need to be taken for
documentation.


Update conda-forge
------------------

Send a PR with the new version number and ``sha256`` hash of the source release
to https://github.com/conda-forge/pywavelets-feedstock.


Create the release on GitHub
----------------------------

On the project's GitHub page, click the releases tab and then press the
"*Draft a new release*" button to create a release from the appropriate tag.


Announcing the release
----------------------

Send release announcements to:

- pywavelets@googlegroups.com
- python-announce-list@python.org
- scipy-user@python.org


Prepare for continued development
---------------------------------

Increment the version number in setup.py and change ISRELEASED to False.

Prepare new release note files for the upcoming release::

    git add doc/release/X.X.X-notes.rst
    git add doc/source/release.X.X.X.rst

And add ``release.X.X.X`` to the list in ``doc/source/releasenotes.rst``
