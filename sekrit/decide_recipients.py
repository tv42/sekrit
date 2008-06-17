from sekrit.get_config import get_config
from sekrit.groups import expand_groups

def decide_recipients(cfg, path):
    sect = get_config(cfg, path)
    if sect is None:
        return []
    users = sect.get('users', '')
    users = users.split(None)
    return expand_groups(cfg, users)
