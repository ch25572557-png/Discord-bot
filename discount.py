from points import get_points

def get_discount(uid):

    pts = get_points(uid)

    if pts >= 100:
        return 0.35
    if pts >= 75:
        return 0.25
    if pts >= 50:
        return 0.15
    if pts >= 25:
        return 0.05

    return 0
