from nose.tools import (
    eq_ as eq,
    assert_raises,
    )

import ConfigParser
from cStringIO import StringIO

from sekrit import groups

def test_non_group():
    cfg = None
    got = groups.expand_groups(cfg, ['foo'])
    eq(sorted(got), sorted(['foo']))

def test_simple():
    cfg = ConfigParser.RawConfigParser()
    cfg.readfp(StringIO("""\
[group bar]
users = quux, thud
"""))
    got = groups.expand_groups(cfg, ['foo', '@bar'])
    eq(sorted(got), sorted(['foo', 'quux', 'thud']))

def test_recursive():
    cfg = ConfigParser.RawConfigParser()
    cfg.readfp(StringIO("""\
[group first]
users = @second, @third

[group second]
users = foo

[group third]
users = bar, @first
"""))
    got = groups.expand_groups(cfg, ['@first'])
    eq(sorted(got), sorted(['foo', 'bar']))

def test_recursive_self():
    cfg = ConfigParser.RawConfigParser()
    cfg.readfp(StringIO("""\
[group bar]
users = foo, @bar
"""))
    got = groups.expand_groups(cfg, ['@bar'])
    eq(sorted(got), sorted(['foo']))
