# Raspberry pi raspbian ros kinetic workspace of pi(no. 38)
# Contact
* Author : Rajendra Singh
* Email  : singh.raj1997@gmail.com
* Web    : https://iamrajee.github.io/
* LinkedIn    : https://www.linkedin.com/in/rajendra-singh-6b0b3a13a/


# File description

* ## refresh.sh
```
#!/bin/bash
source /opt/ros/kinetic/setup.bash
source /home/pi/ros_catkin_ws/devel/setup.bash
source /home/pi/ros_catkin_ws/devel_isolated/setup.bash
clear
```
*It will source the workspace after buiding workspace or after creating new pkg. Run it as `./refresh.sh`*

* ## makefile
```
SHELL=/bin/bash
all:
	make run
run:
	catkin_make #catkin_make_isolated
	bash refresh.sh
```
*It will build the workspace . Run it as `make`*

* ## createpkg.sh
```
#!/bin/bash
cd src/
catkin create $1
cd ../
make
source refresh.sh
```
*It will create new package . Run it as `./createpkg.sh`newpkg_name*

* ## tftree.sh
```
#!/bin/bash
rosrun rqt_tf_tree rqt_tf_tree
```
*It will  launch the gui to visvualise the tf tree. Run it as `./tftree.sh`*

* ## printenv.sh
```
#!/bin/bash
printenv | grep -i ROS
```
*It will print the ROS related environment variable . Run it as `./printenv.sh`*

* ## rosdep.sh
```
sudo rosdep install -i --from-path src --rosdistro kinnetic -y
```
*It will install dependencies of all pkg in the workspace . Run it as `./rosdep.sh`*

* ## rajendra.sh
```
#!/bin/bash
ssh rajendra@rajendra
```
*It will ssh into another system. Useful when using muliple ros masters. Run it as `./rajendra.sh`*

* ## googleassistant.sh
```
#!/bin/bash
{ # try
	googlesamples-assistant-hotword --project-id first-66e46 --device-model-id first-66e46-firstproduct-hx0n7j
	#googlesamples-assistant-pushtotalk --project-id first-66e46 --device-model-id first-66e46-firstproduct-hx0n7j
} || { # catch
    # save log for exception
	bash refresh.sh
}
```
*It will run the googleassistant api in terminal. I used this on RAWBOT 1.0 for audio commads . Run it as `./googleassistant.sh`*


# License
MIT License
Copyright (c) 2019 Rajendra Singh
