#include <stdio.h>

int mem[3000];

int main(){
    int* p;
    p = mem;
    *p = getchar();
    putchar(*p);
    p++;
    p--;
    (*p)++;
    (*p)--;
    while(*p != 0 ){
        (*p)--;
        putchar(*p);
    }
}