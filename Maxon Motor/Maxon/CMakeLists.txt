cmake_minimum_required(VERSION 2.8)
add_definitions(-std=c++11)
project( Maxon_Motor )

include_directories(include)
add_library(MM include/Definitions.h include/cmaxonmotor.h src/cmaxonmotor.cc)
target_link_libraries(MM EposCmd ftd2xx)

add_executable(helloMaxon include/Definitions.h HelloEposCmd.cpp)
target_link_libraries(helloMaxon MM)

add_executable(gaitcycle GaitCycle.cpp)
target_link_libraries(gaitcycle MM)

add_executable(testMaxon motor_test.cpp)
target_link_libraries(testMaxon MM)

add_executable(gait GaitCycleFinal.cpp)
target_link_libraries(gait MM)
