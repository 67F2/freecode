#!/usr/bin/env python3
"""Procedural ASCII action-hero portrait -> assets/avatar.txt.

Pure stdlib. Geometry + light sources sampled onto a character grid,
luminance mapped through a density ramp (' '=brightest, '@'=darkest).
"""

W, H = 64, 34
RAMP = " .:-=+*#%@"

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def blob(x, y, cx, cy, rx, ry):
    """Falloff 0..1, 1 at center."""
    d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
    return clamp(1.0 - d)

def head_halfwidth(y):
    """Half-width of the head/face silhouette at row y."""
    if y < 0.12 or y > 0.99:
        return 0.0
    if y < 0.46:
        t = (y - 0.12) / 0.34
        return 0.305 * (t * (2 - t)) ** 0.5
    if y < 0.72:
        return 0.305
    t = (y - 0.72) / 0.26
    return 0.305 - 0.125 * (t ** 1.6)

def luminance(x, y):
    hw = head_halfwidth(y)
    inside = abs(x - 0.5) <= hw
    if not inside and y < 0.93:
        return 1.0

    L = 1.0

    if y >= 0.93:
        shoulder = clamp((y - 0.93) / 0.07, 0.0, 1.0)
        if abs(x - 0.5) <= 0.10 + 0.40 * shoulder:
            L = 0.10
            if abs(x - 0.5) < 0.045 and y < 0.965:
                L = 0.52
            return L
        return 1.0

    hair_top, hair_bottom = 0.12, 0.325
    if y <= hair_bottom + 0.02:
        L = 0.07
        sheen = blob(x, y, 0.375, 0.185, 0.15, 0.035)
        L += 0.32 * sheen
        if y > hair_bottom:
            fade = 1.0 - (y - hair_bottom) / 0.02
            L = L * fade + 0.66 * (1.0 - fade)
        return clamp(L)

    L = 0.66
    nx = clamp((x - 0.30) / 0.50)
    L -= 0.30 * nx

    L += 0.22 * blob(x, y, 0.43, 0.365, 0.17, 0.055)

    if 0.435 <= y <= 0.468 and not (0.445 <= x <= 0.555):
        L = 0.14

    if 0.475 <= y <= 0.535:
        for ecx, dark in ((0.355, 0.12), (0.645, 0.09)):
            s = blob(x, y, ecx, 0.503, 0.084, 0.040)
            if s > 0:
                L = min(L, 1.0 - s * (1.0 - dark))
        for icx in (0.372, 0.628):
            s = blob(x, y, icx, 0.503, 0.013, 0.011)
            if s > 0:
                L = max(L, 0.60)

    if 0.335 <= y <= 0.468 and hw - abs(x - 0.5) < 0.045:
        L = min(L, 0.30)

    L += 0.10 * blob(x, y, 0.355, 0.565, 0.075, 0.022)

    if 0.475 <= x <= 0.525 and 0.47 <= y <= 0.615:
        L += 0.16
    L -= 0.18 * blob(x, y, 0.548, 0.575, 0.030, 0.085)
    L = min(L, 0.42) if 0.495 <= x <= 0.512 and 0.615 <= y <= 0.635 else L
    L = min(L, 0.40) if blob(x, y, 0.500, 0.625, 0.048, 0.030) > 0.55 else L
    for ncx in (0.455, 0.545):
        if blob(x, y, ncx, 0.658, 0.024, 0.016) > 0.4:
            L = min(L, 0.12)

    L += 0.16 * blob(x, y, 0.300, 0.588, 0.095, 0.050)
    L += 0.03 * blob(x, y, 0.700, 0.588, 0.095, 0.050)

    if 0.716 <= y <= 0.744 and 0.400 <= x <= 0.600:
        L = min(L, 0.44)
    if 0.758 <= y <= 0.774 and 0.420 <= x <= 0.580:
        L = min(L, 0.52)
    if 0.782 <= y <= 0.798 and abs(x - 0.5) < 0.09:
        L = min(L, 0.62)

    L += 0.20 * blob(x, y, 0.500, 0.850, 0.075, 0.038)
    if blob(x, y, 0.500, 0.830, 0.055, 0.028) > 0.5:
        L = max(L, 0.74)

    edge = hw - abs(x - 0.5)
    if edge < 0.028:
        L -= 0.24 * (1.0 - edge / 0.028)

    if y >= 0.88 and 0.425 <= x <= 0.575:
        L = min(L, 0.40)
        if y <= 0.915:
            L = min(L, 0.20)

    return clamp(L)

def main():
    lines = []
    for row in range(H):
        y = (row + 0.5) / H
        line = []
        for col in range(W):
            x = (col + 0.5) / W
            L = luminance(x, y)
            line.append(RAMP[round((1.0 - L) * (len(RAMP) - 1))])
        lines.append("".join(line).rstrip())
    out = "\n".join(lines) + "\n"
    path = __file__.rsplit("/", 2)[0] + "/assets/avatar.txt"
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(out)
    print(out)

if __name__ == "__main__":
    main()
