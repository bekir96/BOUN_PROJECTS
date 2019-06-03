cmake_minimum_required(VERSION 2.8)
project(project2)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp Passenger.cpp Passenger.h Probability.cpp Probability.h)
add_executable(project2 ${SOURCE_FILES})
