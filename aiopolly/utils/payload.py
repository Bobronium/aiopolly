from .case import string_to_camel

DEFAULT_EXCLUDE = {'self', 'cls'}


def generate_params(defaults: dict = None, exclude: set = None, use_camel=True, **kwargs):
    """
    Usage: payload = generate_payload(**locals(), exclude=['foo'], use_camel=False)
    """
    defaults = defaults or {}
    if exclude is None:
        exclude = DEFAULT_EXCLUDE
    else:
        exclude.update(DEFAULT_EXCLUDE)

    params = {}
    for key, value in kwargs.items():
        if key in exclude or key.startswith('_'):
            continue

        if value is None:
            value = defaults.get(key)
            if value is None:
                continue

        elif isinstance(value, dict):
            value = generate_params(**value, exclude=exclude, defaults=defaults)

        elif isinstance(value, list):
            value = [generate_params(**e, exclude=exclude, defaults=defaults)
                     if isinstance(e, dict) else e for e in value]

        params[string_to_camel(key) if use_camel else key] = value

    return params
