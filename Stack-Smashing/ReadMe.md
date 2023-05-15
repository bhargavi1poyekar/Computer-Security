# PCS Project 3: Launch Stack Smashing attack using Buffer overflow mechanism. 

## A.
    * Name: Bhargavi Poyekar
    * UMBC ID: CH33454

## B. Buffer Size: 

    => Last 3 digits: 454
    => Next Boundary aligned to 16 bytes => 464 

## C. Debugger Return Address Computation

    => In the gdb, I added breakpoints at bhargavi and poyekar.
    => Then I started running it. It stopped at first breakpoint i.e bhargavi.
    => I checked the rbp => 0x7fffffffdf60 => The prev value of register is stored here.
    => Then I checked its value and noted it down => 0x7fffffffe000.
    => Then I added 8 bits to this above address, to get the return address. 
    => I noted down the return address. These 2 values are what we have to use for stack corruption.
    => At second breakpoint, I again did the above 2 steps to get the rbp and then I used set to
    change the values. 
    => *0x7fffffffdd60 = 0x7fffffffe000, *0x7fffffffdd68 = 0x5555555552c3
    => This corrupts the stack because in the poyekar function, I am setting the prev value of register 
    and return address which is associated directly to the main function.
    => Hence it skips the bhargavi function and just prints 'Improper Return'.
    => The n is set to n=2 in poyekar, and since it skips bhargavi, n=2 is returned, which goes into 
    the else condition of main function.
    => I used same commands and steps to compute the addresses for part 3, i.e stack 3. But I didn't set the 
    values for corruption in gdb. For part 3 the badfile is used, which is explained in the next part.

## D. Genbadfile:

    => Since my buffer size is 464, I needed to change the same in genbadfile. 
    => Before, the genbadfile was of 96 bytes, so I added 400 X char to it as the same is added for my local buffer.
    => Now, my badfile has 496 bytes, out of which the first 476 bytes are filled with unnecessary data.
    => From [476-479], the value is set as '0x00000001', as we have to return 1 instead of 2. 
    => The return address value and prev register value noted down in gdb is added here.
    => [488-495] is used for the prev value of register => 0x5555555552E4. 
    => [480-487] is used to store the return address. => 0x7fffffffe000.
    => After running the genbadfile.c, the badfile is created with the required values.
    => This badfile, is read by stack3, which overflows the buffer, as the buffer size is only 464 and the badfile size is 496.
    => The buffer overflow, corrupts the stack as required, and then prints only poyekar and returned properly.

## E. Commands Used:

    1. gcc -g -o stack2 -z execstack -fno-stack-protector stack2.c

        => Created the executable file stack2

    2. sudo sysctl -w kernel.randomize_va_space=0

        => It is set to 0, so everytime we run the same code, the stack will assign same addresses.

    3. gdb stack2

        Part 1:
        => run 

           To run it without any changes. (Part 1)

        Part 2:
        => b bhargavi

           Adds a breakpoint at bhargavi

        => b poyekar
         
            Adds a breakpoint at poyekar

        => run

           Then run the code.

        => p $rbp

           After stopping at breakpoint bhargavi, I check the value of $rbp.

        => x/2wx 0x7fffffffdf60

           Then I checked the address rbp is pointing to and note it down. 

        => x/2wx 0x7fffffffdf68

           Then I checked value of prev register and noted it down.

        => c

           continues the code.

        => p $rbp
        
           After stopping at breakpoint poyekar, I check the value of $rbp.

        => set *0x7fffffffdd60 = 0x7fffffffe000

           Change the prev register value to the value noted down before for corrupting the stack.

        => set *0x7fffffffdd68 = 0x5555555552c3

           Change the return address to the value noted down before for corrupting the stack.

        => c

           Continue 

        => quit

           Quit debugging mode.

    5. gdb stack3.c

        => b bhargavi
        => run
        => p $rbp
        => x/2wx 0x7fffffffddd0
        => x/2wx 0x7fffffffddd8
        => quit

    6. gcc -g -o genbadfile -z execstack -fno-stack-protector genbadfile.c

        Create executable genbadfile

    7. ./genbadfile

        Execute genbadfile => this creates badfile

    8. gcc -g -o stack3 -z execstack -fno-stack-protector stack3.c

        Create executable stack3

    9. gdb stack3.c 

        => run

            Run the stack3 in gdb.

## F. Bonus Question:

1. I tried to follow the same strategy of changing the return address and prev value of rbp using c coding.
2. I was able to find the return address and prev value of rbp of bhargavi, but I was not able to modify 
those values of poyekar.
3. I then tried an another method of skipping bhargavi function by adding the size of bhargavi's frame to 
return address of poyekar.
4. I found rbp value using builtin frame address and *(rbp + 1) indicates the return address, then I added 
0x28 which is 40 in decimal (frame size for bhargavi), which I found by gdb. So, by doing this,
I directly jump to return of bhargavi.


## G. Challenges Faced:

1. While performing the step3, modifying the stack values using file input, I was facing problem in 
making the changes. Then I tried debugging what I was doing wrong and then I understood that I didn't 
change the size of char x in main and the same in the fread, which was causing actual problem.

2. I faced challenge in the bonus question. I am able to calculate the return address of function bhargavi(foo)
and also the prev add, but I am not able to modify the values. 

## H. Summary:

1. I understood how stack works. 
2. I understood how the return address and prev value of rbp is required while calling and returning to a function.
3. I understood how we can corrupt the stack through debugger and with the help of file.

## I. References:

1. Professor's document for exercise.
2. https://www.tutorialspoint.com/c_standard_library/c_function_fread.htm
3. https://manpages.ubuntu.com/manpages/trusty/man1/gdb.1.html#:~:text=You%20can%20use%20GDB%20to,using%20the%20command%20%22help%22.
4. https://www.tutorialspoint.com/cprogramming/c_pointers.htm
5. https://gcc.gnu.org/onlinedocs/gcc/Return-Address.html




    

    
    

            

