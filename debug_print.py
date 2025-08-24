from shared import debug_mode, debug_mode_rating

def debug_print(*args, **kwargs):
    if debug_mode:
        print(*args, **kwargs)

def debug_rating_print(*args, **kwargs):
    if debug_mode_rating:
        print(*args, **kwargs)