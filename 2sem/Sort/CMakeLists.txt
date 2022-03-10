cmake_minimum_required(VERSION 3.22)
project(Sort)

set(CMAKE_CXX_STANDARD 20)

add_executable(Sort
        heapsort.cpp
        qsort.cpp
        main.cpp)