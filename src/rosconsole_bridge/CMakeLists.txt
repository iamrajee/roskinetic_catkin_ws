cmake_minimum_required(VERSION 2.8.3)
project(rosconsole_bridge)

find_package(console_bridge REQUIRED)
find_package(catkin REQUIRED COMPONENTS rosconsole)

include_directories(include ${catkin_INCLUDE_DIRS} ${console_bridge_INCLUDE_DIRS})
link_directories(${catkin_LIBRARY_DIRS} ${console_bridge_LIBRARY_DIRS})

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS rosconsole
  DEPENDS console_bridge
)

add_library(${PROJECT_NAME} src/bridge.cpp)

target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES} ${console_bridge_LIBRARIES})

install(
  TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
)

install(
  DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION})

if(CATKIN_ENABLE_TESTING)
  add_subdirectory(test)
endif()
