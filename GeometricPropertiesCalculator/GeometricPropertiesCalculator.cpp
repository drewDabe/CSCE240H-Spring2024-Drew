#include <iostream>
#include <fstream>
#include <cmath>
#include <string>

using namespace std;

double calculateRectangleArea(double length, double width) {
    return length * width;
}

double calculateRectanglePerimeter(double length, double width) {
    return 2 * (length + width);
}

double calculateCircleArea(double radius) {
    return M_PI * radius * radius;
}

double calculateCirclePerimeter(double radius) {
    return 2 * M_PI * radius;
}

double calculateTriangleArea(double side1, double side2, double side3) {
    double s = (side1 + side2 + side3) / 2.0;
    return sqrt(s * (s - side1) * (s - side2) * (s - side3));
}

double calculateTrianglePerimeter(double side1, double side2, double side3) {
    return side1 + side2 + side3;
}

int main() {
    ifstream inputFile("C:\\Users\\kerry\\cppprojs\\GeometricPropertiesCalculator\\input.txt");
    ofstream outputFile("C:\\Users\\kerry\\cppprojs\\GeometricPropertiesCalculator\\output.txt");

    if (!inputFile.is_open() || !outputFile.is_open()) {
        cerr << "Error opening files!" << endl;
        return 1;
    }

    string shape;
    double property;
    while (inputFile >> shape) {
        if (shape == "RECTANGLE") {
            double length, width;
            inputFile >> length >> width;
            inputFile >> property;

            if (property == 1) {
                double area = calculateRectangleArea(length, width);
                outputFile << "RECTANGLE AREA " << area << endl;
            } else if (property == 2) {
                double perimeter = calculateRectanglePerimeter(length, width);
                outputFile << "RECTANGLE PERIMETER " << perimeter << endl;
            }
        } else if (shape == "CIRCLE") {
            double radius;
            inputFile >> radius;
            inputFile >> property;

            if (property == 1) {
                double area = calculateCircleArea(radius);
                outputFile << "CIRCLE AREA " << area << endl;
            } else if (property == 2) {
                double perimeter = calculateCirclePerimeter(radius);
                outputFile << "CIRCLE PERIMETER " << perimeter << endl;
            }
        } else if (shape == "TRIANGLE") {
            double side1, side2, side3;
            inputFile >> side1 >> side2 >> side3;
            inputFile >> property;

            if (property == 1) {
                double area = calculateTriangleArea(side1, side2, side3);
                outputFile << "TRIANGLE AREA " << area << endl;
            } else if (property == 2) {
                double perimeter = calculateTrianglePerimeter(side1, side2, side3);
                outputFile << "TRIANGLE PERIMETER " << perimeter << endl;
            }
        }
    }

    inputFile.close();
    outputFile.close();

    return 0;
}