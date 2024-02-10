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

Change ``ISRELEASED`` to ``True`` in ``util/version_utils.py`` and commit.

Tag the release via::

    git tag -s vX.X.X

Then push the ``vX.X.X`` tag to the PyWavelets GitHub repo.

Build Windows, OS X and Linux wheels and upload to PyPI
-------------------------------------------------------

Pushing the vX.X.X tag to the repository will kick off automated build and
deployment of the wheels to PyPI. The wheel builds proceed via GitHub Actions
and their status can be checked by going to the Actions tab on GitHub.

In the event that the automated deployment fails, the built wheels can be
downloaded via the GitHub Actions artifacts and then uploaded manually using
twine as described below.

Create the source distribution
------------------------------

The automated wheel build process should also automatically upload the sdist
to PyPI. In the event that automated upload of the sdist fails, please proceed
in generating and uploading it manually as described in this section.

Remove untracked files and directories with ``git clean``.
*Warning: this will delete files & directories that are not under version
control so you may want to do a dry run first by adding -n, so you can see what
will be removed*::

    git clean -xfdn

Then run without ``-n``::

    git clean -xfd

Create the source distribution file via::

    python -m build --sdist


Upload the release to PyPI
--------------------------

These instructions cover how to upload wheels and source distributions to PyPI
in the event that the automated deployment fails. The binary Windows wheels downloaded from GitHub Actions (see above) should also be placed into the
``/dist`` subfolder along with the sdist archives.

The wheels and source distributions created above can all be securely uploaded
to pypi.python.org using twine::

    twine upload -s dist/*

Note that the documentation on ReadTheDocs (http://pywavelets.readthedocs.org)
will have been automatically generated, so no actions need to be taken for
documentation.


Update conda-forge
------------------

The is an autotick bot run by conda-forge that is likely to autodetect the new
PyPI release and autogenerate a PR for you that will update the PyWavelets
feedstock for conda-forge. If this automated PR does not appear, you will need
to send a PR with the new version number and ``sha256`` hash of the source
release to https://github.com/conda-forge/pywavelets-feedstock.


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

Increment the version number in ``util/version_utils.py`` and change
``ISRELEASED`` to False.

Prepare new release note files for the upcoming release::

    git add doc/release/X.X.X-notes.rst
    git add doc/source/release.X.X.X.rst

And add ``release.X.X.X`` to the list in ``doc/source/releasenotes.rst``
