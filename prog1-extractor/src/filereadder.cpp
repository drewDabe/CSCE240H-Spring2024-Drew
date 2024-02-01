#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
#include <algorithm> // Included for std::count_if

// Function to count words, lines, and characters in a given text for each part
void countTextStatistics(const std::string& filename) {
    std::ifstream inputFile(filename);

    if (!inputFile.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }

    std::string line;
    bool countStarted = false;
    bool countEnded = false;

    int partNumber = 0;
    int partMax = 4;
    int wordCount = 0;
    int lineCount = 0;
    int charCount = 0;


    bool tablecontent = false;
    //Clear table of contents first before everything
    while (std::getline(inputFile, line)) {
        if (line.find("PART I") != std::string::npos && !tablecontent) {
            tablecontent = true; //Table of contents has started
            continue;
        }
        if(tablecontent) {
            if (line.find("PART V") != std::string::npos) { //Means there are 5 Parts instead of 4
                partMax = 5;
            }
            if (line == "PART I") {
                break; //Actual content found
            }
        }
    }

    while (std::getline(inputFile, line) && partNumber <= partMax) {
        // Probably a better way without tablecontent for later
        if (line.find("PART") != std::string::npos || tablecontent) {
            tablecontent = false;
            // Found a line containing "PART", start counting for the next part
            if (countStarted) {
                // Display statistics for the current part
                std::cout << "Part " << partNumber << " - Word count: " << wordCount << ", Line count: " << lineCount << ", Character count: " << charCount << std::endl;
            }

            // Reset counts for the next part
            wordCount = 0;
            lineCount = 0;
            charCount = 0;
            countStarted = true;
            partNumber++;
        } else if (countStarted) {
            // Count words, lines, and characters for the current part
            wordCount += std::count_if(line.begin(), line.end(), ::isspace);
            charCount += line.length();
            lineCount++;
        }
    }

    // Display statistics for the last part
    std::cout << "Part " << partNumber << " - Word count: " << wordCount << ", Line count: " << lineCount << ", Character count: " << charCount << std::endl;
}

int main() {
    // Replace "tsla.txt" with the whatever file wanting to count (could also do multiple)
    countTextStatistics("./tsla.txt");

    return 0;
}
