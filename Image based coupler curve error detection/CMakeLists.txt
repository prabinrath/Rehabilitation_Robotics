cmake_minimum_required(VERSION 2.8)
add_definitions(-std=c++11)
project( image_error_detection )
find_package( OpenCV REQUIRED )

add_executable( error_detect error_detect.cpp )
target_link_libraries( error_detect ${OpenCV_LIBS} -lpthread)
