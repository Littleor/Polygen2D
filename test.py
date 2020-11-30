from Polygen2D import Point, Line, Polygen
import numpy as np
x = np.array([0, 5, 5, 0])
y = np.array([0, 0, 5, 5])
points: [Point] = [] # 多边形点集
for i in range(len(x)):
  points.append(Point(x=x[i],y=y[i]))
polygen = Polygen(points) # 多边形初始化
test_point1 = Point(x=1, y=1)
test_point2 = Point(x=-1, y=-1)
test_point3 = Point(x=5, y=2)
test_line = Line(test_point1, test_point2)
print("test_point1 In Polygen?", polygen.contain(test_point1)) # 判断test_point1是否在多边形内
print("test_point2 In Polygen?", polygen.contain(test_point2)) # 判断test_point2是否在多边形内
print("the distance between test_point3 and test_line:", test_line.distance(test_point3)) # 点test_point3到线test_line的距离