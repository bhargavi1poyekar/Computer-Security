#include <stdio.h>
#include <string.h>

// bar -> replaced with my last name -> poyekar
int poyekar(char *str) {
  char bx[464];
  /* bx size changed-> 64 replaced with 464 -> the next 16 byte
  boundary of my umbc id last 3 digits (454)
  */
  int n = 2;
  
  strcpy(bx, str);
  puts("poyekar");
  
  //Number of bytes used by bhargavi function is added to rbp+1, where the return address is stored, so it goes directly to the return of bhargavi. 
  unsigned long long *rbp =(unsigned long long *)__builtin_frame_address(0);
  *(rbp+1)+=0x28;
  
  return n;
  
  
}

// foo replaced with  my first name -> bhargavi
int bhargavi(char *str) {
 
  char fx[464];
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
