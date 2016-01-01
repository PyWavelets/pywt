Guidelines for Releasing PyWavelets
===================================

The following are guidelines for preparing a release of PyWavelets.  The
notation vX.X.X in the commands below would be replaced by the actual release
number.


updating the release notes
--------------------------
Prior to the release, make sure the release notes are up to date.

author lists can be generated via:

```python  ./util/authors.py vP.P.P..```
(where vP.P.P is the previous release number)

and the lists of Issues closed and PRs merged via:

```python ./util/gh_lists.py vX.X.X```  (script requires Python 2.X to run)


Tag the release and trigger the build of Windows wheels
-------------------------------------------------------

Change ISRELEASED to TRUE in `setup.py` and commit.

Appveyor will build wheels for windows.  If the commit with ISRELEASED=True
is submitted as a PR, the wheels can be downloaded from appveyor once it has
run on the PR.  They can be found under the "Artifacts" tab in the Appveyor
interface.  These should be downloaded so that they can later be uploaded to
pypi.python.org.


Tag the release via:

```git tag -s vX.X.X```

Then push the vX.X.X tag to master.


Create the source distribution
------------------------------

Remove untracked files and directories via git clean.
**Warning:**  This will delete files & directories that are not under version
control so you may want to do a dry run first by adding -n, so you can see what
will be removed:

```git clean -xfdn```

Then run without -n:

```git clean -xfd```

Create the source distribution files via:

```python setup.py sdist --formats=gztar,zip```


Upload the release to pypi
--------------------------

The binary Windows wheels downloaded from Appveyor (see above) should
also be placed into the /dist subfolder along with the sdist archives.

The wheels and source distributions created above can all be securely uploaded
to pypi.python.org using twine:

```twine upload -s dist/*```


Upload the documentation to pypi
--------------------------------
The documentation on readthedocs (http://pywavelets.readthedocs.org) will have
been automatically generated, but the documentation linked from pypi.python.org
(http://pythonhosted.org/PyWavelets/) will need to be manually updated.  This
can be done by building the documentation locally and zipping 'doc/build/html'
so that index.html is at the top level of the archive. This archive can then be
uploaded in the "files" section of the PyWavelets page on pypi.


Create the release on GitHub
----------------------------
On the project's github page, click the releases tab and then press the
"Draft a new release" button to create a release from the appropriate tag.


Announcing the release
----------------------

Send release announcements to:

- https://groups.google.com/forum/#!forum/pywavelets  (pywavelets@googlegroups.com)
- python-announce-list@python.org
- scipy-user@scipy.org


Prepare for continued development
---------------------------------

Increment the version number in setup.py and change ISRELEASED to False.

Prepare new release note files for theupcoming release:

```
git add doc/release/X.X.X-notes.rst
git add doc/source/release.X.X.X.rst
```

And add release.X.X.X to the list in:

``` doc/source/releasenotes.rst ```
