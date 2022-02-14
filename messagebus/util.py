from typing import Union


# TODO Might not be the best name as it returns a string and not a Path
def get_class_path(obj: Union[str, type, object]):
    if obj is None:
        return obj
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, type):
        return f"{obj.__module__}.{obj.__name__}"
    else:
        return f"{obj.__module__}.{obj.__class__.__name__}"
