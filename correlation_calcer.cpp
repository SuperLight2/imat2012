#include <iostream>
#include <stdio.h>
#include <string>

using namespace std;

vector<string> splitCharBuf(char* buf, char delimiter) {
    vector<string> result;
    string currentString = "";
    size_t length = Strlen(buf);
    for (int i = 0; i < length; ++i) {
        if (buf[i] == delimemter) {
            if (currentString != "")
                result.push_back(currentString);
            currentString = "";
        } else {
            currentString += buf[i];
        }
    }
    if (currentString != "")
        result.push_back(currentString);
       return result;
}

int main(int argc, char** argv) {
    string descriptionFilepath = argv[1];
    string poolFilepath = argv[2];
    char buf[10000];

    cerr << descriptionFilepath << " " << poolFilepath << endl;
    vector<string> descriptions;

    FILE* descriptionFile = open(descriptionFilepath.c_str(), 'r');
    while (!eof(descriptionFile)) {
        fgets(descriptionFile, buf);
        vector<string> s = splitCharBuf(buf, '\t');
    }

    return 0;
}
