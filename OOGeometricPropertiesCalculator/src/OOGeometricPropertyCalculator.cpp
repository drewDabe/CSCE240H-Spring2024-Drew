#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include "Rectangle.h"
#include "Circle.h"
#include "Triangle.h"

using namespace std;

void processShape(const string& shapeType, double arg1, double arg2 = 0, double arg3 = 0, int choice = 0) {
    Shape* shape = nullptr;
    if (shapeType == "RECTANGLE") {
        shape = new Rectangle(arg1, arg2);
    } else if (shapeType == "CIRCLE") {
        shape = new Circle(arg1);
    } else if (shapeType == "TRIANGLE") {
        shape = new Triangle(arg1, arg2, arg3);
    }

    if (shape != nullptr) {
        if (choice == 1) {
            shape->calculateArea();
        } else if (choice == 2) {
            shape->calculatePerimeter();
        }

        ofstream outputFile("C:\\Users\\kerry\\cppprojs\\OOGeometricPropertiesCalculator\\data\\output.txt", ios::app);
        if (outputFile.is_open()) {
            if (shape->getErrorMessage() != "") {
                outputFile << shapeType << " " << (choice == 1 ? "AREA" : "PERIMETER") << " " << shape->getErrorMessage() << endl;
            } else {
                outputFile << shapeType << " " << (choice == 1 ? "AREA" : "PERIMETER") << " " << (choice == 1 ? shape->getArea() : shape->getPerimeter()) << endl;
            }
            outputFile.close();
        } else {
            cerr << "Unable to open output file." << endl;
        }
        delete shape;
    } else {
        cerr << "Invalid shape type." << endl;
    }
}

int main() {
    int choice;
    while (true) {
        ifstream inFile("C:\\Users\\kerry\\cppprojs\\OOGeometricPropertiesCalculator\\data\\input.txt");
        if (!inFile.is_open()) {
            cerr << "Unable to open input file." << endl;
            return 1;
        }
        cout << "Enter 1 for AREA or 2 for PERIMETER. Enter any other key to quit: ";
        cin >> choice;
        if (choice != 1 && choice != 2) {
            break;
        }
        string line;
        while (getline(inFile, line)) {
            istringstream iss(line);
            string shapeType;
            iss >> shapeType;
            
            if (shapeType == "RECTANGLE") {
                double length, breadth;
                if (iss >> length >> breadth) {
                    processShape(shapeType, length, breadth, 0, choice);
                } else {
                    cerr << "Invalid input for rectangle." << endl;
                }
            } else if (shapeType == "CIRCLE") {
                double radius;
                if (iss >> radius) {
                    processShape(shapeType, radius, 0, 0, choice);
                } else {
                    cerr << "Invalid input for circle." << endl;
                }
            } else if (shapeType == "TRIANGLE") {
                double side1, side2, side3;
                if (iss >> side1 >> side2 >> side3) {
                    processShape(shapeType, side1, side2, side3, choice);
                } else {
                    cerr << "Invalid input for triangle." << endl;
                }
            } else {
                cerr << "Invalid shape type." << endl;
            }
        }
        inFile.close();
    }

    

    return 0;
}
