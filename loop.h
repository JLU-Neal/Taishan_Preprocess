#include<iostream>

using namespace std;
extern "C"{
   void test(); 
   void func(int16_t*i , int16_t*j, int8_t step, int16_t ij_length, int16_t width, int16_t height, int8_t* img);
}
