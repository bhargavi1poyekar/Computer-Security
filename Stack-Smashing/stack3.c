#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// bar -> replaced with my last name -> poyekar
int poyekar(char *str) {
  FILE *fd;
  char bx[464];
  int n = 2;
  /* bx size changed-> 64 replaced with 464 -> the next 16 byte
  boundary of my umbc id last 3 digits (454)
  */

  fd = fopen("badfile", "r");
  fread(bx, sizeof(char), 528, fd); 
  // Changed 128 to 528 as we are increasing the bx size by 400 and then copying it to str.
  strcpy(str, bx);
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
  puts("bhargavi");
  return n;
}

int main() {
  char x[528] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  // Changed 128 to 528 as we are increasing the bx size by 400 and then copying it to str.
  FILE *fd;
  int n;

  n = bhargavi(x);

  if (n == 1) {
    printf("Returned properly\n");
  } else {
    printf("Improper return \n");
  }

  return 0;
}
