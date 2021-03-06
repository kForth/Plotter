import time
import cProfile

def create_distinct_colours(num_colours):
    for i in range(num_colours):
        hue = i / (num_colours)
        saturation = 0.5
        luminance = 0.5
        rgb = hsl_to_rgb(hue, saturation, luminance)
        yield rgb

def hue_to_rgb(p, q, t):
    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1 / 6:
        return p + (q - p) * 6 * t
    if (t < 1 / 2):
        return q
    if (t < 2 / 3):
        return p + (q - p) * (2 / 3 - t) * 6
    return p;
    

def hsl_to_rgb(h, s, l):
    r = 0
    b = 0
    g = 0

    if s == 0:
        r = l
        b = l
        g = l
    else:
        q = (l * (1 + s)) if l < 0.5 else (l + s - l * s)
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1 / 3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1 / 3)

    return int(r * 255), int(g * 255), int(b * 255)

def fmod(num, mod):
    if mod > num or mod == 0 or num == 0:
        return num
    num_sign = 1 if num >= 0 else -1
    num = abs(num)
    mod = abs(mod)
    while num >= mod:
        num -= mod
    return num * num_sign

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        print('{} took {}ms'.format(f.__name__, (time.time() - start) * 1000))
        return result
    return f_timer

def profilefunc(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort='time')
    return profiled_func