from nose.tools import (
    eq_ as eq,
    )

from sekrit.match_path import match_path

def test_simple_mismatch():
    assert not match_path('foo', 'bar')

def test_exact():
    assert match_path('foo', 'foo')

def test_exact_dirs():
    assert match_path('foo/bar', 'foo/bar')

def test_wildcard_full():
    assert match_path('foo', '*')

def test_wildcard_partial():
    assert match_path('foobar', 'fo*ar')

def test_wildcard_slashes():
    assert match_path('foo/bar', 'foo/*')

def test_wildcard_matches_slashes():
    assert match_path('foo/bar', 'fo*ar')

def test_prefix_wrong_way():
    assert not match_path('foo/bar/baz', 'bar/baz')

def test_prefix():
    # we want "example.com" to match "example.com/foo"
    assert match_path('foo/bar/baz', 'foo/bar')
    assert not match_path('foo/barbaz', 'foo/bar')
