using namespace std;
#include <fstream>
#include <iostream>
#include <vector>
#include <stack>
#include <map>

char mem[3000];

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Sourcefile argument is required");
        exit(1);
    }
    fstream in(argv[1]);
    vector<char> sourcecode;
    while (in.peek() != EOF) {
        char op;
        in >> op;
        sourcecode.push_back(op);
    }

    stack<int> branches;
    map<int, int> jumpForward;
    map<int, int> jumpBackward;

    for (int i = 0; i < sourcecode.size(); i++) {
        if (sourcecode[i] == '[') {
            branches.push(i);
        }
        else if (sourcecode[i] == ']') {
            int openBracketPos = branches.top();
            branches.pop();
            jumpForward[openBracketPos] = i;
            jumpBackward[i] = openBracketPos;
        }
    }

    char *ptr = mem;
    int programCounter = 0;
    while (programCounter < sourcecode.size()) {
        switch (sourcecode[programCounter]) {
        case '>':
            ptr++;
            break;
        case '<':
            ptr--;
            break;
        case '+':
            (*ptr)++;
            break;
        case '-':
            (*ptr)--;
            break;
        case '.':
            cout << (*ptr);
            break;
        case ',':
            cin >> (*ptr);
            break;
        case '[':
            if ((*ptr) == 0) {
                programCounter = jumpForward[programCounter];
            }
            break;
        case ']':
            programCounter = jumpBackward[programCounter] - 1;
            break;
        default:
            break;
        }
        programCounter ++;
    }

    sourcecode.clear();
    return 0;
}