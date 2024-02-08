#include "Shape.h"

Shape::Shape() : area(0), perimeter(0), errorMessage("") {}

Shape::~Shape() {}

double Shape::getArea() {
    return area;
}

double Shape::getPerimeter() {
    return perimeter;
}

std::string Shape::getErrorMessage() {
    return errorMessage;
}
