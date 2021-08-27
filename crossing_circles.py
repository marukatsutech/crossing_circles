# Crossing points of circles (animation)
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches


def circumscribed_point(p0, r0, p1, r1):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    ratio = r0 / (r0 + r1)
    return (
        (p0[0] + dx * ratio), (p0[1] + dy * ratio)
    )


def inscribed_point(p0, r0, p1, r1):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    ratio = - r0 / (r1 - r0)
    return (
        (p0[0] + dx * ratio), (p0[1] + dy * ratio)
    )


def circles_cross_points(p0, r0, p1, r1, d):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    ratio = r0 / d
    v = (dx * ratio, dy * ratio)    # Vector from p0 to p1 as same length as r0
    cos_alpha = (r0**2 + d**2 - r1**2) / (2 * r0 * d)   # Cosine formula
    sin_alpha = math.sqrt(1 - cos_alpha**2)
    rot_plus = np.array([[cos_alpha, - sin_alpha], [sin_alpha, cos_alpha]])  # Matrix of rotation
    rot_minus = np.array([[cos_alpha, sin_alpha], [- sin_alpha, cos_alpha]])  # Matrix of reverse rotation
    v_plus = np.dot(rot_plus, v)    # rotate
    v_minus = np.dot(rot_minus, v)
    return (
        (p0[0] + v_plus[0], p0[1] + v_plus[1]),
        (p0[0] + v_minus[0], p0[1] + v_minus[1])
    )


def draw_crossing_points(cross_status, p0, r0, p1, r1, d):
    if cross_status == 2:
        cp = circumscribed_point(p0, r0, p1, r1)
        circle_cp = patches.Circle(xy=cp, radius=cp_r, color="red")
        ax.add_patch(circle_cp)
    elif cross_status == 3:
        cp = inscribed_point(p0, r0, p1, r1)
        circle_cp = patches.Circle(xy=cp, radius=cp_r, color="red")
        ax.add_patch(circle_cp)
    elif cross_status == 6:
        cp0, cp1 = circles_cross_points(p0, r0, p1, r1, d)
        circle_cp0 = patches.Circle(xy=cp0, radius=cp_r, color="red")
        circle_cp1 = patches.Circle(xy=cp1, radius=cp_r, color="red")
        ax.add_patch(circle_cp0)
        ax.add_patch(circle_cp1)
    else:
        pass


def get_cross_status(d, r0, r1):
    if abs(r0 - r1) <= tolerance and d <= tolerance:    # r0 == r1 and d = 0
        return 1  # Match
    else:
        if abs(d - (r0 + r1)) <= tolerance:  # d == r0 + r1
            return 2  # Circumscribed circles
        elif abs(abs(r0 - r1) - d) <= tolerance:  # abs(r0 - r1) == d
            return 3  # Inscribed circles
        else:
            if d > (r0 + r1):  # d > r0 + r1
                return 4  # Not cross
            elif abs(r0 - r1) > d:  # abs(r0 - r1) > d
                return 5  # Not cross (Included circles)
            elif abs(r0 - r1) < d < abs(r0 + r1):   # abs(r0 - r1) < d < r0 + r1
                return 6  # Cross
            else:
                return 0    # Error


def set_axis():
    ax.set_title("Crossing points of circles")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal")
    ax.grid()


def update(f):
    ax.cla()    # Clear ax
    set_axis()
    ax.text(x_min, y_max * 0.9, "Step=" + str(f))

    # Draw circle0
    global point0, v0, radius0, change_radius0
    circle0 = patches.Circle(xy=point0, radius=radius0, fill=False)
    ax.add_patch(circle0)

    # Draw circle1
    global point1, v1, radius1, change_radius1
    circle1 = patches.Circle(xy=point1, radius=radius1, fill=False)
    ax.add_patch(circle1)

    # Draw crossing points
    pv = point1 - point0  # Vector from p0 to p1
    d = np.linalg.norm(pv, 2)  # Norm of vector pv
    cross_status = get_cross_status(d, radius0, radius1)
    # print(cross_status, d)
    draw_crossing_points(cross_status, point0, radius0, point1, radius1, d)

    # Move and change radius of circle0
    point0 = point0 + v0
    # Reverse vector if out out of range
    if point0[0] > x_max or point0[0] < x_min:
        v0 = np.dot(reverse_h, v0)
    if point0[1] > y_max or point0[1] < y_min:
        v0 = np.dot(reverse_v, v0)
    r0 = radius0 + change_radius0  # Change radius
    if r0 > r_max or r0 < r_min:
        change_radius0 = -change_radius0

    # Move and change radius of circle1
    point1 = point1 + v1    # Change position
    # Reverse vector if out out of range
    if point1[0] > x_max or point1[0] < x_min:
        v1 = np.dot(reverse_h, v1)
    if point1[1] > y_max or point1[1] < y_min:
        v1 = np.dot(reverse_v, v1)
    radius1 = radius1 + change_radius1   # Change radius
    if radius1 > r_max or radius1 < r_min:
        change_radius1 = -change_radius1


# Global variables setting
x_min = -10.
x_max = 10.
y_min = -10.
y_max = 10.
w = x_max - x_min
h = y_max - y_min
r_max = 10.
r_min = 1.
reverse_h = np.array([[-1, 0], [0, 1]])  # Matrix of horizontal reverse
reverse_v = np.array([[1, 0], [0, -1]])  # Matrix of vertical reverse

radius0 = np.random.rand() * w / 2 * 0.9 + 1.
radius1 = np.random.rand() * w / 2 * 0.9 + 1.
change_radius0 = 0.1
change_radius1 = 0.1
point0 = np.array([np.random.rand() * w - w / 2, np.random.rand() * h - h / 2])     # Initial points of circles
point1 = np.array([np.random.rand() * w - w / 2, np.random.rand() * h - h / 2])
theta0 = np.random.rand() * 2. * math.pi    # Angle of motion
theta1 = np.random.rand() * 2. * math.pi
s0 = 0.5    # Scalar of velocity
v0 = s0 * np.array([math.cos(theta0), math.sin(theta0)])    # Vector of circles
v1 = s0 * np.array([math.cos(theta1), math.sin(theta1)])

tolerance = 1 / 1000000
cp_r = min([x_max - x_min, y_max - y_min]) * 0.01   # Radius of crossing points

# Prepare figure and axes
fig = plt.figure()
ax = fig.add_subplot(111)

# Draw animation
set_axis()
anim = animation.FuncAnimation(fig, update, interval=100)
plt.show()
