import sys, os, pytest, json

from Repository import Repository  # pylint: disable=import-error
from Database import Database      # pylint: disable=import-error

def test_create(with_database):
  repository = Repository.create("path")
  assert repository.path == "path"

def test_get_by_path(with_database):
  Repository.create("/hello/world")
  assert Repository.get_by_path("/hello/world").path == "/hello/world"

def test_assigns_all_fields(with_database):
  repo = Repository.create("blah")

  assert repo.repositoryID is not None
  assert repo.path is not None

def test_get_all_repositories(with_database):
  repo = Repository.create("blah")

  repos = Repository.get_all()
  reponames = [repo.path for repo in repos if repo]
  assert set(["blah", "."]) == set(reponames)