#ifndef SHAPE_H
#define SHAPE_H

#include <string>

class Shape {
protected:
    double area;
    double perimeter;
    std::string errorMessage;

public:
    Shape();
    virtual ~Shape();
    virtual void calculateArea() = 0;
    virtual void calculatePerimeter() = 0;
    double getArea();
    double getPerimeter();
    std::string getErrorMessage();
};

#endif // SHAPE_H
