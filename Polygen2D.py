from decimal import Decimal
import numpy as np


class Point:
    # 通过坐标初始化
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

    def mov(self, x=0, y=0):
        self.x += x
        self.y += y

    # 点到点的距离
    def distance(self, point):
        return abs(np.sqrt(np.square(self.x - point.x) + np.square(self.y - point.y)))


class Line:

    def __init__(self, p1, p2):
        # y = kx + b型直线
        self.p1 = p1
        self.p2 = p2
        if self.is_horizontal():
            self.k = Decimal('0')
            self.b = self.p1.y
        elif self.is_vertical():
            self.k = None
            self.b = None
        else:
            self.k = (p2.y - p1.y) / (p2.x - p1.x)
            self.b = -p1.x * (p2.y - p1.y) / (p2.x - p1.x) + p1.y

    # 求点到线的距离
    def distance(self, point: Point):
        if self.is_horizontal():
            return abs(point.y - self.p1.y)
        if self.is_vertical():
            return abs(point.x - self.p1.x)
        (APx, APy) = (point.x - self.p1.x, point.y - self.p1.y)
        (ABx, ABy) = (self.p2.x - self.p1.x, self.p2.y - self.p1.y)
        r = (APx * ABx + APy * ABy) / np.sqrt(np.square(ABx) + np.square(ABy))
        if r <= 0:
            return point.distance(self.p1)
        if r >= 1:
            return point.distance(self.p2)
        if self.k is None and self.b is None:
            return abs(point.x - self.p1.x)
        if self.k is None and self.b is not None:
            return abs(point.y - self.p1.y)
        return abs((self.k * point.x - point.y + self.b) / np.sqrt(np.square(self.k) + 1))

    def get_horizontal_distance_with_point(self, point: Point):
        if self.is_vertical():
            return abs(point.x - self.p1.x), Point(x=self.p1.x, y=point.y)
        if self.is_horizontal():
            # 无穷
            return 10000000
        return abs(point.x - (point.y - self.b) / self.k), Point(x=(point.y - self.b) / self.k, y=point.y)

    def get_vertical_distance_with_point(self, point: Point):
        if self.is_vertical():
            # 无穷
            return 10000000
        if self.is_horizontal():
            return abs(point.y - self.p1.y), Point(x=point.x, y=(self.p1.y))
        return abs(point.y - (self.k * point.x + self.b)), Point(x=point.x, y=(self.k * point.x + self.b))

    # 求两条线的相交点
    # 有的话return Point没有的话return None
    def intersection(self, line2):
        # 两直线平行
        if self.is_vertical() and line2.is_vertical():
            return None
        if self.is_horizontal() and line2.is_horizontal():
            return None
        if self.k == line2.k:
            return None
        # 相交
        # 有其中一条垂直
        if self.is_vertical() and not line2.is_vertical():
            x = self.p1.x
            y = line2.k * x + line2.b
        elif line2.is_vertical() and not self.is_vertical():
            x = line2.p1.x
            y = self.k * x + self.b
        elif line2.is_horizontal() and not self.is_horizontal():
            y = line2.p1.y
            x = (y - self.b) / self.k
        elif self.is_horizontal() and not line2.is_horizontal():
            y = self.p1.y
            x = (y - line2.b) / line2.k
        else:
            # 一般情况
            x = (self.b - line2.b) / (line2.k - self.k)
            y = self.k * x + self.b

        # 点在线段上：x在线段的范围内
        r1 = (self.p2.x, self.p1.x) if self.p1.x >= self.p2.x else (self.p1.x, self.p2.x)
        r2 = (line2.p2.x, line2.p1.x) if line2.p1.x >= line2.p2.x else (line2.p1.x, line2.p2.x)

        ry1 = (self.p2.y, self.p1.y) if self.p1.y >= self.p2.y else (self.p1.y, self.p2.y)
        ry2 = (line2.p2.y, line2.p1.y) if line2.p1.y >= line2.p2.y else (line2.p1.y, line2.p2.y)

        if not (ry1[0] <= y <= ry1[1] and ry2[0] <= y <= ry2[1] and r1[0] <= x <= r1[1] and r2[0] <= x <= r2[1]):
            return None

        return Point(x, y)

    def is_horizontal(self):

        return self.p1.y == self.p2.y

    def is_vertical(self):

        return self.p1.x == self.p2.x

    def __repr__(self):
        return "[{}->{}, k={}, b={}]".format(self.p1, self.p2, self.k, self.b)


class Polygen:

    def __init__(self, points: [Point]):

        self.points: [Point] = points
        self.lines = []
        if len(points) > 0:
            for i in range(0, len(points) - 1):
                self.lines.append(Line(points[i], points[i + 1]))
            self.lines.append(Line(points[-1], points[0]))

    def get_min_x_point(self):
        min = 1000
        min_point = None
        for p in self.points:
            if p.x < min:
                min = p.x
                min_point = p
        return min_point

    def get_min_y_point(self):
        min = 1000
        min_point = None
        for p in self.points:
            if p.y < min:
                min = p.y
                min_point = p
        return min_point

    def remove_last_point(self):
        self.points = self.points[:-1]
        self.lines = self.lines[:-2]
        self.lines += [Line(self.points[-2], self.points[-1]), Line(self.points[-1], self.points[0])]

    def add_point(self, point: Point, index=-1):
        if index == -1 or index == len(self.points) - 1:
            self.points.append(point)
            if len(self.lines) > 1:
                self.lines = self.lines[0:-1]
            else:
                self.lines = []
            if len(self.points) > 1:
                self.lines.append(Line(self.points[-2], self.points[-1]))
                self.lines.append(Line(self.points[-1], self.points[0]))
        else:
            self.points.insert(index, point)
            self.lines[index] = Line(self.points[index], self.points[index + 1])
            self.lines.insert(index, Line(self.points[index + 1], self.points[index + 2]))

    def has_intersection(self, point):
        for i in range(len(self.lines) - 1):
            if self.lines[i].intersection(Line(point, self.points[-1])) is not None:
                return (self.lines[i].intersection(Line(point, self.points[-1])), self.lines[i])
        return None

    def remove_after(self, point):
        # print("出现了交点",point)
        for i in range(len(self.points)):
            if self.points[i] == point:
                self.points = self.points[:i + 1]
                self.lines = self.lines[:i + 1]
                self.lines.append(Line(self.points[-1], self.points[0]))
                break

    def remove_between(self, p1: Point, p2: Point):
        begin_index = -1
        end_index = -1
        for i in range(len(self.points)):
            if self.points[i] == p1:
                begin_index = i
            if self.points[i] == p2:
                end_index = i
            if begin_index != -1 and end_index != -1:
                break
        if begin_index == -1 or end_index == -1:
            return
        self.points = self.points[:min(begin_index, end_index) + 1] + self.points[
                                                                      max(begin_index, end_index):]
        self.lines = self.lines[:min(begin_index, end_index) + 1] + self.lines[
                                                                    max(begin_index,
                                                                        end_index):]

    def replace_between(self, p1: Point, p2: Point, replace_point: Point):
        begin_index = -1
        end_index = -1
        for i in range(len(self.points)):
            if self.points[i] == p1:
                begin_index = i
            if self.points[i] == p2:
                end_index = i
            if begin_index != -1 and end_index != -1:
                break
        if begin_index == -1 or end_index == -1:
            return
        self.points = self.points[:min(begin_index, end_index) + 1] + [replace_point] + self.points[
                                                                                        max(begin_index, end_index):]
        self.lines = self.lines[:min(begin_index, end_index) + 1] + [Line(p1, replace_point),
                                                                     Line(replace_point, p2)] + self.lines[
                                                                                                max(begin_index,
                                                                                                    end_index):]

    # 判断点是否包含在多边形内
    def contain(self, point):
        return len(self.get_same_y_line(point)) > 0 and len(self.get_same_x_line(point)) > 0

    # 获取和该点在同一个高度上的线
    def get_same_y_line(self, point) -> [Line]:
        lines = []
        points = []
        for line in self.lines:
            r = (line.p2.y, line.p1.y) if line.p1.y >= line.p2.y else (line.p1.y, line.p2.y)
            if (r[0] <= point.y <= r[1]) and line.p1 not in points and line.p2 not in points:
                # 认为这个线在y值上覆盖了点的y值
                points.append(line.p1)
                points.append(line.p2)
                lines.append(line)
        lines = sorted(lines, key=lambda s: (s.p1.x + s.p2.x) / 2, reverse=False)
        x_mean_list = [(line.p1.x + line.p2.x) / 2 for line in lines]
        return x_mean_list

    # 获取和该点在同一个高度上的线
    def get_same_x_line(self, point) -> [Line]:
        lines = []
        point_a = Point(point.x, point.y - 100000)
        point_b = Point(point.x, point.y + 100000)
        line2 = Line(point, point_b)
        line3 = Line(point, point_a)
        points = []
        for line in self.lines:
            r = (line.p2.x, line.p1.x) if line.p1.x >= line.p2.x else (line.p1.x, line.p2.x)
            if (r[0] <= point.x <= r[1]) and line.p1 not in points and line.p2 not in points:
                # 认为这个线在y值上覆盖了点的y值
                points.append(line.p1)
                points.append(line.p2)
                lines.append(line)
        lines = sorted(lines, key=lambda s: (s.p1.y + s.p2.y) / 2, reverse=False)
        y_mean_list = [((line.p1.y + line.p2.y) / 2) for line in lines]
        return y_mean_list

    # 获取点到多边形状的最短距离和最短的线
    def min_distance(self, point):
        if not self.contain(point):
            return None
        min = 100000000
        min_line = None

        for line in self.lines:
            distance = line.distance(point)
            if min > distance:
                min = distance
                min_line = line
        if min_line is None:
            return None
        return (min, min_line)

