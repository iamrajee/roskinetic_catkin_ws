REM generated from ros_environment/env-hooks/1.ros_etc_dir.bat.em

@[if DEVELSPACE]@
REM env variable in develspace
set ROS_ETC_DIR=@(CATKIN_DEVEL_PREFIX)/@(CATKIN_GLOBAL_ETC_DESTINATION)/ros
@[else]@
REM env variable in installspace
set ROS_ETC_DIR=@(CMAKE_INSTALL_PREFIX)/@(CATKIN_GLOBAL_ETC_DESTINATION)/ros
@[end if]@
