# Polygen2D

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

- [背景](#背景)
- [安装](#安装)
- [示例](#示例)
- [更多](更多 )
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [使用许可](#使用许可)

## 背景

在使用Python处理2D散点图时，发现当下Python库中对平面坐标系的少之又少，想要对点、线、多边形进行操作和判断实在不方便，**Polygen2D**应运而生，**Polygen2D**旨在解决2D平台下对散点的处理，将散点抽象为多边形等。

## 安装

这个项目基于Python3。请确保你本地安装的Python版本大于3。

```sh
$ pip install Polygen2D
$ # pip3 install Polygen2D # 如果使用的是pip3
```

## 示例

这里的参考程序通过Numpy生成了多边形数据点后生成对应的点、线和面来进行判断点是否在多边形内、计算点到线的距离。

```python
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
```

## 更多

如果想要将散点图生成具体图像可以借助[matplotlib](https://github.com/matplotlib/matplotlib)来实现。

## 维护者

[@Littleor](https://github.com/Littleor)。

## 如何贡献

非常欢迎你的加入！[提一个 Issue](https://github.com/Littleor/Polygen2D/issues/new) 或者提交一个 Pull Request。


标准 Readme 遵循 [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) 行为规范。


## 使用许可

[MIT](LICENSE) © Littleor
