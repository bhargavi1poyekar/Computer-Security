#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// bar -> replaced with my last name -> poyekar
int poyekar(char *str) {
  char bx[464];
  /* bx size changed-> 64 replaced with 464 -> the next 16 byte
  boundary of my umbc id last 3 digits (454)
  */
  int n = 2;

  strcpy(bx, str);
  puts("poyekar");
  return n;
}

// foo replaced with my first name -> bhargavi
int bhargavi(char *str) {
  char fx[464];
  /* fx size changed-> 64 replaced with 464 -> the next 16 byte
  boundary of my umbc id last 3 digits (454)
  */
  int n = 1;

  poyekar(str);
  strcpy(fx, str);
  puts("bhargavi");
  return n;
}

int main() {
  char x[128] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  
  int n;

  n = bhargavi(x);
  //replaced foo with my first name

  if (n == 1) {
    printf("Returned properly\n");
  } else {
    printf("Improper return \n");
  }

  return 0;
}
