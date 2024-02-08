#ifndef TRIANGLE_H
#define TRIANGLE_H

#include "Shape.h"

class Triangle : public Shape {
private:
    double side1;
    double side2;
    double side3;

public:
    Triangle(double s1, double s2, double s3);
    ~Triangle();
    void calculateArea() override;
    void calculatePerimeter() override;
};

#endif // TRIANGLE_H
