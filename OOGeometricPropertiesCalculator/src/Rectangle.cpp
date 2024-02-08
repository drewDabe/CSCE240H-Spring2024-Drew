#include "Rectangle.h"

Rectangle::Rectangle(double l, double b) : length(l), breadth(b) {}

Rectangle::~Rectangle() {}

void Rectangle::calculateArea() {
    if (length >= 0 && breadth >= 0) {
        area = length * breadth;
    } else {
        errorMessage = "Invalid values passed for rectangle.";
    }
}

void Rectangle::calculatePerimeter() {
    if (length >= 0 && breadth >= 0) {
        perimeter = 2 * (length + breadth);
    } else {
        errorMessage = "Invalid values passed for rectangle.";
    }
}
