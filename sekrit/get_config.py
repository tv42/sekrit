from sekrit import match_path

def get_config(cfg, path):
    found = None
    for section in cfg.sections():
        (type, glob) = section.split(None, 1)
        if type != 'access':
            continue
        if not match_path.match_path(
            path=path,
            glob=glob,
            ):
            continue
        if found is None:
            found = {}
        found.update(cfg.items(section))

    return found

