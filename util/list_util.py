__all__ = ['one_layer']

# 只保留1层list
def one_layer(_list):
    if isinstance(_list[0],list):
        return one_layer(_list[0])
    return _list