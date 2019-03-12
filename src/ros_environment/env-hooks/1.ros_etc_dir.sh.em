# generated from ros_environment/env-hooks/1.ros_etc_dir.sh.em

@[if DEVELSPACE]@
# env variable in develspace
export ROS_ETC_DIR="@(CATKIN_DEVEL_PREFIX)/@(CATKIN_GLOBAL_ETC_DESTINATION)/ros"
@[else]@
# env variable in installspace
if [ -z "$CATKIN_ENV_HOOK_WORKSPACE" ]; then
  CATKIN_ENV_HOOK_WORKSPACE="@(CMAKE_INSTALL_PREFIX)"
fi
export ROS_ETC_DIR="$CATKIN_ENV_HOOK_WORKSPACE/@(CATKIN_GLOBAL_ETC_DESTINATION)/ros"
@[end if]@
