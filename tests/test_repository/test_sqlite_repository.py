from bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest
from dataclasses import dataclass
from bookkeeper.models.category import Category


@dataclass
class TestModel:
    pk: int = 0
    comment: str = ''


@pytest.fixture
def custom_class():
    return TestModel


@pytest.fixture
def repo():
    return SQLiteRepository('test.db', TestModel)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_nonexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.comment = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'pk': 1}) == [objects[0]]
    assert repo.get_all({'comment': 'test'}) == objects
