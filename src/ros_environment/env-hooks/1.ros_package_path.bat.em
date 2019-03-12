REM generated from ros_environment/env-hooks/1.ros_package_path.bat.em

REM python function to generate ROS package path based on all parent workspaces (prepends the separator if necessary)
REM do not use EnableDelayedExpansion here, it messes with the != symbols
setlocal disabledelayedexpansion
echo from __future__ import print_function > _parent_package_path.py
echo import os >> _parent_package_path.py
echo env_name = 'CATKIN_WORKSPACES' >> _parent_package_path.py
echo items = os.environ[env_name].split(';') if env_name in os.environ and os.environ[env_name] != '' else [] >> _parent_package_path.py
echo path = '' >> _parent_package_path.py
echo for item in items: >> _parent_package_path.py
echo     path += ':' + (os.path.join(item, 'share') if item.find(':') == -1 else item.split(':')[1]) >> _parent_package_path.py
echo print(path) >> _parent_package_path.py
endlocal

setlocal EnableDelayedExpansion

set ROS_PACKAGE_PATH_PARENTS=
for /f %%a in ('@(PYTHON_EXECUTABLE) _parent_package_path.py') do set ROS_PACKAGE_PATH_PARENTS=!ROS_PACKAGE_PATH_PARENTS!%%a

@[if DEVELSPACE]@
REM env variable in develspace
set ROS_PACKAGE_PATH=@(CMAKE_SOURCE_DIR)!ROS_PACKAGE_PATH_PARENTS!
@[else]@
REM env variable in installspace
set ROS_PACKAGE_PATH=@(CMAKE_INSTALL_PREFIX)/share;@(CMAKE_INSTALL_PREFIX)/stacks;%ROS_PACKAGE_PATH_PARENTS%
@[end if]@

del _parent_package_path.py

REM Make sure the variable survives local scope
endlocal && set ROS_PACKAGE_PATH=%ROS_PACKAGE_PATH%
