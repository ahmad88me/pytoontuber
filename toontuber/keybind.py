"""
This file is to be used later for custom key bindings
"""

key_bindings = dict()
for i in range(10):
    key_bindings[str(i)] = str(i)


def get_action(char):
    if char in key_bindings:
        return key_bindings[char]
    return None


