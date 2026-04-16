from points import get_points, remove_points

def get_discount(points):

    if points >= 100:
        return 0.35, 100
    elif points >= 75:
        return 0.25, 75
    elif points >= 50:
        return 0.15, 50
    elif points >= 25:
        return 0.05, 25

    return 0, 0


def apply(user_id, total):

    pts = get_points(user_id)

    d, cost = get_discount(pts)

    final = total - (total * d)

    if cost:
        remove_points(user_id, cost)

    return int(final), d, cost
