from nose.tools import (
    eq_ as eq,
    )

import ConfigParser
from cStringIO import StringIO

from sekrit import decide_recipients

def test_simple():
    cfg = ConfigParser.RawConfigParser()
    cfg.readfp(StringIO("""\
[access *]
users = @bar xyzzy

[group bar]
users = quux thud
"""))
    got = decide_recipients.decide_recipients(cfg, 'some/path')
    eq(sorted(got), sorted(['quux', 'thud', 'xyzzy']))
