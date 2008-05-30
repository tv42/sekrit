from nose.tools import (
    eq_ as eq,
    )

from cStringIO import StringIO

from sekrit import (
    ordered_config_parser,
    get_config,
    )

def test_example():
    cfg = ordered_config_parser.OrderedRawConfigParser()
    cfg.readfp(StringIO("""\
[access */@root]
users = @admins

[access client.com/*]
users = @staff

[access client.com/foo/@root]
users = @admins, @project-foo

# overrides!
[access example.com/*/@root]
users = @trusted

# overrides!
[access example.com/vip/@root]
users = @really-trusted
"""))

    got = get_config.get_config(cfg, 'client.com/server1/@user')
    eq(got, dict(users='@staff'))

    got = get_config.get_config(cfg, 'client.com/server1/@root')
    eq(got, dict(users='@staff'))

    got = get_config.get_config(cfg, 'client.com/foo/@user')
    eq(got, dict(users='@staff'))

    got = get_config.get_config(cfg, 'client.com/foo/@root')
    eq(got, dict(users='@admins, @project-foo'))

    got = get_config.get_config(cfg, 'example.com/bar/@root')
    eq(got, dict(users='@trusted'))

    got = get_config.get_config(cfg, 'example.com/vip/@root')
    eq(got, dict(users='@really-trusted'))

    got = get_config.get_config(cfg, 'example.com/bar/@something-else')
    eq(got, None)
