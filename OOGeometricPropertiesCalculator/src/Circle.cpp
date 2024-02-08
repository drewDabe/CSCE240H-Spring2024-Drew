#include "Circle.h"
#define _USE_MATH_DEFINES
#include <cmath>

Circle::Circle(double r) : radius(r) {}

Circle::~Circle() {}

void Circle::calculateArea() {
    if (radius >= 0) {
        area = M_PI * radius * radius;
    } else {
        errorMessage = "Invalid radius passed for circle.";
    }
}

void Circle::calculatePerimeter() {
    if (radius >= 0) {
        perimeter = 2 * M_PI * radius;
    } else {
        errorMessage = "Invalid radius passed for circle.";
    }
}
