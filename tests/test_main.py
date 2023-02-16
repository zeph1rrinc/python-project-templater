"""Tests module"""
from os.path import join, exists
from shutil import rmtree

import pathlib
import pytest

from python_project_templater.main import create_project


def test_error():
    """Testing if create project raising value error for undefined template"""
    with pytest.raises(ValueError):
        create_project("123", "123")


@pytest.mark.parametrize("test_project_path,template", [
    (join(pathlib.Path(__file__).parent.resolve(), "test-base"), "base")
])
def test_create_project(test_project_path, template):
    """Testing normal project creating"""
    assert create_project(template, test_project_path)
    assert exists(test_project_path)
    assert exists(join(test_project_path, ".git"))
    rmtree(test_project_path)
