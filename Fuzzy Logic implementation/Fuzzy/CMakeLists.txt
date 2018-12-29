cmake_minimum_required(VERSION 2.8)
add_definitions(-std=c++11)
project( Fuzzy )

include_directories(include)
add_library(Fuzzy include/fuzzy_controller.h src/fuzzy_controller.cpp)
add_executable(fuzz test_fuzzy.cpp)
target_link_libraries(fuzz Fuzzy)

