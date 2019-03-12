# How can we ensure that the binary goes to build dir only, not devel dir?
add_executable(cleanup cleanup.cpp)
target_link_libraries(cleanup rosconsole_bridge)
add_test(NAME cleanup COMMAND cleanup)
