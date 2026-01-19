import os
import sys

import click
import spin
from spin.cmds import meson


@click.command()
@click.option(
    '--tests', '-t',
    default=None, metavar='TESTS', multiple=True,
    help="Which tests to run"
)
@click.option(
    '--compare', '-c',
    is_flag=True,
    default=False,
    help="Compare benchmarks between the current branch and main "
         "(unless other branches specified). "
         "The benchmarks are each executed in a new isolated "
         "environment."
)
@click.option(
    '--verbose', '-v', is_flag=True, default=False
)
@click.option(
    '--quick', '-q', is_flag=True, default=False,
    help="Run each benchmark only once (timings won't be accurate)"
)
@click.option(
    '--factor', '-f', default=1.05,
    help="The factor above or below which a benchmark result is "
         "considered reportable. This is passed on to the asv command."
)
@click.argument(
    'commits', metavar='',
    required=False,
    nargs=-1
)
@meson.build_dir_option
@click.pass_context
def bench(ctx, tests, compare, verbose, quick, factor, commits, build_dir):
    """🏋 Run benchmarks.

    \b
    Examples:

    \b
    $ spin bench -t dwt_benchmarks
    $ spin bench -t swt_benchmarks.Swt2TimeSuite.time_swt2

    Two benchmark runs can be compared.
    By default, `HEAD` is compared to `main`.
    You can also specify the branches/commits to compare:

    \b
    $ spin bench --compare
    $ spin bench --compare main
    $ spin bench --compare main HEAD

    You can also choose which benchmarks to run in comparison mode:

    $ spin bench -t Swt2TimeSuite --compare

    For a quicker but less accurate check to see if benchmarks work:

    $ spin bench --quick

    """
    if not commits:
        commits = ('main', 'HEAD')
    elif len(commits) == 1:
        commits = commits + ('HEAD',)
    elif len(commits) > 2:
        raise click.ClickException(
            'Need a maximum of two revisions to compare'
        )

    bench_args = []
    for t in tests:
        bench_args += ['--bench', t]

    if verbose:
        bench_args = ['-v'] + bench_args

    if quick:
        bench_args = ['--quick'] + bench_args

    if not compare:
        # No comparison requested; we build and benchmark the current version

        click.secho(
            "Invoking `build` prior to running benchmarks:",
            bold=True, fg="bright_green"
        )
        ctx.invoke(meson.build)

        meson._set_pythonpath(build_dir)
        # Some weird bug, not sure what's going on here, but it seems necessary
        # on Python 3.14
        if not os.environ['PYTHONPATH'].endswith(os.sep):
            os.environ['PYTHONPATH'] += os.sep

        p = spin.util.run(
            [sys.executable, '-c', 'import pywt; print(pywt.__version__)'],
            cwd='benchmarks',
            echo=False,
            output=False
        )
        pywt_ver = p.stdout.strip().decode('ascii')

        click.secho(
            f'Running benchmarks on PyWavelets {pywt_ver}',
            bold=True, fg="bright_green"
        )
        cmd = [
            'asv', 'run', '--dry-run', '--show-stderr', '--python=same'
        ] + bench_args

        os.chdir('..')
        spin.util.run(cmd, cwd='benchmarks', env=os.environ)
    else:
        # Ensure that we don't have uncommitted changes
        commit_a, commit_b = (_commit_to_sha(c) for c in commits)

        if commit_b == 'HEAD' and _dirty_git_working_dir():
            click.secho(
                "WARNING: you have uncommitted changes --- "
                "these will NOT be benchmarked!",
                fg="red"
            )

        cmd_compare = [
            'asv', 'continuous', '--factor', str(factor),
        ] + bench_args + [commit_a, commit_b]
        spin.util.run(cmd_compare, cwd='benchmarks')


def _commit_to_sha(commit):
    p = spin.util.run(['git', 'rev-parse', commit], output=False, echo=False)
    if p.returncode != 0:
        raise (
            click.ClickException(
                f'Could not find SHA matching commit `{commit}`'
            )
        )

    return p.stdout.decode('ascii').strip()


def _dirty_git_working_dir():
    # Changes to the working directory
    p0 = spin.util.run(['git', 'diff-files', '--quiet'])

    # Staged changes
    p1 = spin.util.run(['git', 'diff-index', '--quiet', '--cached', 'HEAD'])

    return (p0.returncode != 0 or p1.returncode != 0)
