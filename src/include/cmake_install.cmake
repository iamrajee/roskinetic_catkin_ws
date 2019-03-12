# Install script for directory: /home/pi/ros_catkin_ws/src/opencv3/include

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pi/ros_catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv-3.3.1-dev/opencv" TYPE FILE FILES
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/cv.h"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/cv.hpp"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/cvaux.h"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/cvaux.hpp"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/cvwimage.h"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/cxcore.h"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/cxcore.hpp"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/cxeigen.hpp"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/cxmisc.h"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/highgui.h"
    "/home/pi/ros_catkin_ws/src/opencv3/include/opencv/ml.h"
    )
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv-3.3.1-dev/opencv2" TYPE FILE FILES "/home/pi/ros_catkin_ws/src/opencv3/include/opencv2/opencv.hpp")
endif()

