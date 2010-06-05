from nose.tools import (
    eq_ as eq,
    )

import ConfigParser
from cStringIO import StringIO

from sekrit import user_to_fpr

from sekrit.test.util import assert_raises

def test_simple():
    cfg = ConfigParser.RawConfigParser()
    cfg.readfp(StringIO("""\
[fingerprints]
jdoe = B18D D37D 391B D037 B668  A32A C447 4F3C 620F 3B4B
"""))
    got = user_to_fpr.user_to_fpr(cfg, 'jdoe')
    eq(got, 'B18DD37D391BD037B668A32AC4474F3C620F3B4B')

def test_not_found():
    cfg = ConfigParser.RawConfigParser()
    cfg.readfp(StringIO("""\
[fingerprints]
jdoe = B18D D37D 391B D037 B668  A32A C447 4F3C 620F 3B4B
"""))
    e = assert_raises(
        user_to_fpr.UnknownUserError,
        user_to_fpr.user_to_fpr,
        cfg, 'smith',
        )
    eq(str(e), 'Unknown user: smith')
