cmake_minimum_required(VERSION 2.8)
project(project3)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O2")

set(SOURCE_FILES main.cpp Graph.h Graph.cpp)
add_executable(project3 ${SOURCE_FILES})
