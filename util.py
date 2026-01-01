def dict_access(dictionary, keys, default=None):
    current = dictionary
    for key in keys:
        current = current[key]
        if current is None:
            return default
        return current

def title_access(name):
    title = ""
    if name.get('english') is not None:
        title = name.get('english')
    elif name.get('romaji') is not None:
        title = name.get('romaji')
    elif name.get('native') is not None:
        title = name.get('native')
    return title