from __future__ import with_statement

import logging
import os
from cStringIO import StringIO

from nose.tools import (
    eq_ as eq,
    )

from sekrit.test.util import (
    assert_raises,
    maketemp,
    )

from sekrit import (
    verify,
    ordered_config_parser,
    )

def test_simple():
    data = """
-----BEGIN PGP MESSAGE-----
Version: GnuPG v1.4.6 (GNU/Linux)

hQIOA/JiGU+GKWbNEAf+Mj23UceAZbB0F1aiM7/3JJdoEqKqof1L/zdPU3YF1STX
dcGVrERNgLgxk8hheLQUSrTOZ9THhQuFmkWkBkB6NKOn5pElxAOWmB04496Q+Fux
xXiNA/CHdlgRzrYj22WErmuUgbv8mIMBDrEcIhj775d2aXiBr864AN+LpP6l/3XR
t0jbIdf6JbswN0e/Vwgw6i1JWSl62vYHpuD9fOzoVrCdiwNAVBAun1bYmZAYAA/F
1fGIwfNaD4z3AXzapkYcctu3KBn9sd2NewRicDTdHTEXBrN3HNfkjU0HAHaP8vGI
hNNnFGwEcbm/CWfU8Q6wXozZQty/6jhYcop0yZJzcgf/dtmQ9fAdnfVraSggbM1v
yEwZq6OHGgBHHWrET6YQ/QG7MgZOEHQSBemaD6qvB4QLc/8nxhZrZG6GOXDz5QbO
1HFDEcmlwN3gWPypMCJlJ+rHdWkaU9Bap8JuULGUZZ+VUeQI0MBWYwaeweIL5/5+
xT8XPa+Ez74EInxbNwEGzLNpjy6m8zaLFaWHu52cS7sRaYrhv1Nj1oW6XcVNhYAY
d/yMrNLqUfpKF0pqb4WVV1b1tqi4igNP9Cl9GWs2QBSbiabFsJZjwoFT7IhXlZJl
79R+zV37OUM5RhR0KuHvfvqKka3hyiOyi/pNOPnUeZ+0WxDILWIZHEF3LS4a7+sN
8oUCDgPwUTneWoUOhRAH/3O5H0+Pby76M6I/i0OdmGmrSHbUl++M/+XCLX8qVfDe
AKf9n8tzsWb1tO7uVs1NivsGmWSToZ9o45fQd9k5pwwr/tE3oyCbtFgkmtKLlPrP
6dMXUjlF8sRk3KCGUPAOa69/Y0USSQ5M6HVj9TFeS9lrUOnyy570wX6nuwM1lKuB
4t8zg/LnZgUSfHXdUmJJGUjAP0ppsmrWKnqTtdtIMbUhwKhKGWXBHXvpII/u97ED
BJ3hFEDs0gjeSk1OU79pzQ8fz2/ZXifm8IYYyNQ3a0eA0EjRNaGF3Xgr9jI+Pwku
cTQZV1cw0YTajXgXHxA/N6ddi035psLjaqTrfq2Sk2UH+gNpfJdvI8YTwCWsf01b
ACoWxNf7GyNrLUjjo6P2kSG27H1IvyBdkL48ghFw2vR3/k6B059I27CLbKDn20as
e6BgJnMea8aqIhbLbPQtfW2OnlfWCyOx2HTUa2F+zGpqWADX9r6J8hnQVjsBD1FG
0TGmCHIqe+BCsBXERdFU3fJh1JjZg5rvdo+gpZ4CAuOupBfrH0f5h7pcQb8oKhLP
wxgYpMGYsElS2ioyam/EqO45fMh1p+tJ/kGPb5sL20ORJc63knW1olI04VEzjY87
esl3/iBHiZ+YKKasJum3KD4gfkglW955Igj+9pUNI73hvoN83yXuhIbOPicZg3Hh
zHTSPwHRiwIVoo8ULFoRdUxgdL9zUdVz/+7R+pyaIQ4RVvQz0QFXH3rjDBow0N1n
QXbPbHR4+golsi6vouzOp7VIrQ==
=0e7b
-----END PGP MESSAGE-----
"""
    tmp = maketemp()
    path = os.path.join(tmp, 'message')
    with file(path, 'w') as f:
        f.write(data)

    cfg = ordered_config_parser.OrderedRawConfigParser()
    cfg.readfp(StringIO("""\
[access message]
users = tv esa

[fingerprints]
tv = DB74559E2AB7C126FACAA3C4947509D4251AA7AB
esa = 8208 9CF0 7AAB AAC2 C25D  9C70 407A 5DA8 04F6 4D37
"""))

    log = logging.getLogger('sekrit.verify')
    log.setLevel(logging.DEBUG)
    buf = StringIO()
    handler = logging.StreamHandler(buf)
    handler.setLevel(logging.INFO)
    log.addHandler(handler)
    try:
        got = verify.verify(cfg=cfg, path=tmp)
    finally:
        log.removeHandler(handler)
    eq(got, True)
    handler.flush()
    eq(
        buf.getvalue().splitlines(),
        [
            'message: ok: esa tv',
            ],
        )
