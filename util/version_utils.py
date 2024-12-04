import argparse
import os
import subprocess

MAJOR = 1
MINOR = 8
MICRO = 0
ISRELEASED = True
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


def get_version_info(source_root):
    # Adding the git rev number needs to be done inside
    # write_version_py(), otherwise the import of pywt.version messes
    # up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists(os.path.join(source_root, '.git')):
        GIT_REVISION = git_version(source_root)
    elif os.path.exists('pywt/version.py'):
        # must be a source distribution, use existing version file
        # load it as a separate module to not load pywt/__init__.py
        import runpy
        ns = runpy.run_path('pywt/version.py')
        GIT_REVISION = ns['git_revision']
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev0+' + GIT_REVISION

    return FULLVERSION, GIT_REVISION


def write_version_py(source_root, filename='pywt/version.py'):
    cnt = """\
# THIS FILE IS GENERATED DURING THE PYWAVELETS BUILD
# See util/version_utils.py for details

short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    FULLVERSION, GIT_REVISION = get_version_info(source_root)

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()


# Return the git revision as a string
def git_version(cwd):
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               env=env, cwd=cwd).communicate()[0]
        return out

    try:
        git_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        git_dir = os.path.join(git_dir, ".git")
        out = _minimal_ext_cmd(['git',
                                '--git-dir',
                                git_dir,
                                'rev-parse',
                                'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')[:7]
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=str, default='.',
                        help="Relative path to the root of the source directory")
    args = parser.parse_args()

    write_version_py(args.source_root)
