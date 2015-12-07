#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from invoke import run, task
from invoke.util import log

from py.path import local


@task
def clean():
    """clean - remove build artifacts."""
    for dirname in ['build',
                    'dist',
                    'vanguard.egg-info',
                    "{{ cookiecutter.repo_name|replace('-', '_') }}.egg-info"]:
        dirpath = local(dirname)
        if dirpath.exists():
            dirpath.remove(rec=1)
    for mask in ["__pycache__", "*.pyc", "*.pyo", "*~"]:
        map(local.remove, local().visit(mask))

    log.info('cleaned up')


@task
def test():
    """test - run the test runner."""
    run('py.test --flakes --cov-report html --cov {{ cookiecutter.repo_name|replace('-', '_') }} tests/', pty=True)
    run('open htmlcov/index.html')


@task
def lint():
    """lint - check style with flake8."""
    run('flake8 {{ cookiecutter.repo_name|replace('-', '_') }} tests')


@task(clean)
def publish():
    """publish - package and upload a release to the cheeseshop."""
    run('python setup.py sdist upload', pty=True)
    run('python setup.py bdist_wheel upload', pty=True)

    log.info('published new release')
