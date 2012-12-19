#include <iostream>
#include <stdio.h>
#include <string>
#include <vector>
#include <cmath>

using namespace std;

vector<string> splitCharBuf(char* buf, char delimeter) {
    vector<string> result;
    string currentString = "";
    size_t length = strlen(buf);
    for (int i = 0; i < length; ++i) {
        if (buf[i] == delimeter) {
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

bool startsWith(const string& text, const string& prefix) {
    if (text.length() < prefix.length())
        return false;
    for (int i = 0; i < prefix.length(); ++i)
        if (text[i] != prefix[i])
            return false;
    return true;
}

int main(int argc, char** argv) {
    string descriptionFilepath = argv[1];
    string poolFilepath = argv[2];
    char buf[10000];
    vector< pair<string, string> > descriptions;

    FILE* descriptionFile = fopen(descriptionFilepath.c_str(), "r");
    while (!feof(descriptionFile)) {
        fgets(buf, 10000, descriptionFile);
        vector<string> s = splitCharBuf(buf, '\t');
        descriptions.push_back(make_pair(s[0], s[1]));
    }

    vector<double> sum_1, sum_2;
    vector< vector<double> > prod, C;
    size_t linesCount = 0;

    FILE* poolFile = fopen(poolFilepath.c_str(), "r");
    while (!feof(poolFile)) {
        ++linesCount;
        fgets(buf, 10000, poolFile);
        vector<string> sString = splitCharBuf(buf, '\t');
        vector<double> s;
        for (int i = 0; i < sString.size(); ++i) {
            s.push_back(atof(sString[i].c_str()));
        }
        if (sum_1.size() == 0) {
            sum_1.assign(s.size(), 0);
            sum_2.assign(s.size(), 0);
            prod.assign(s.size(), vector<double>(s.size(), 0));
            C.assign(s.size(), vector<double>(s.size(), 0));
        }
        for (int i = 0; i < descriptions.size(); ++i) {
            sum_1[i] += s[i];
            sum_2[i] += s[i] * s[i];
            for (int j = i + 1; j < descriptions.size(); ++j) {
                prod[i][j] += s[i] * s[j];
            }
        }
        if (linesCount % 100000 == 0)
            cerr << linesCount << endl;
    }

    for (int i = 0; i < descriptions.size(); ++i) {
        for (int j = i + 1; j < descriptions.size(); ++j) {
            if (startsWith(descriptions[i].second, "asnwer!") && !startsWith(descriptions[j].second, "asnwer!") || 1==1) {
                C[i][j] = (linesCount * prod[i][j] - sum_1[i] * sum_1[j]);
                if (fabs(linesCount * sum_2[i] - sum_1[i]) > 1e-8 && fabs(linesCount * sum_2[j] - sum_1[j]) > 1e-8) {
                    C[i][j] /= sqrt((double)linesCount * sum_2[i] - sum_1[i]);
                    C[i][j] /= sqrt((double)linesCount * sum_2[j] - sum_1[j]);
                } else {
                    C[i][j] = 0;
                }
                cout << descriptions[i].first << "\t" << descriptions[j].first << "\t";
                printf("%.6lf\n", fabs(C[i][j]));
            }
        }
    }

    return 0;
}
