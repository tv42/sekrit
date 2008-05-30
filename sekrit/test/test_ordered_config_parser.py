from nose.tools import (
    eq_ as eq,
    )

from cStringIO import StringIO

from sekrit import ordered_config_parser

def test_simple():
    cfg = ordered_config_parser.OrderedRawConfigParser()
    data = StringIO("""\
[foo]
[fake9]
[fake8]
[fake7]
[fake6]
[fake5]
[fake4]
[fake3]
[fake2]
[fake1]
[bar]
""")
    cfg.readfp(data)
    got = cfg.sections()
    want = [
        'foo',
        'fake9',
        'fake8',
        'fake7',
        'fake6',
        'fake5',
        'fake4',
        'fake3',
        'fake2',
        'fake1',
        'bar',
        ]
    eq(sorted(got), sorted(want), 'test is broken')
    eq(got, want)
