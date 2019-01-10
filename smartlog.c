#include <stdio.h>

enum color {
  black, 
  red,     
  green, 
  yellow, 
  blue,  
  magenta, 
  cyan,  
  white
};

const char *colorOf(int code) {
  printf("\033[0;%dm", 30+code);
}

void flag(int code, const char *msg) {
  printf("[");
}


int main() {
  int i;
  for(i=0; i<8; i++) {
    colorize(red);
    printf("x");
  }
  printf("\n");
}
