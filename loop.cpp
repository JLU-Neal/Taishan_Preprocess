#include"loop.h"
#include<stdint.h>

void test()
{
    cout<<"C++ Extension Working!"<<endl;
}

void func(int16_t*i , int16_t*j, int8_t step, int16_t ij_length, int16_t height, int16_t width, int8_t* img)
{
    
    for (int16_t index = 0; index < ij_length; index+=step)
    {
        img[i[index]*width + j[index]]++;       
    }
    
}