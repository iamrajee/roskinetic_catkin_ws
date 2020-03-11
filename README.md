# Raspberry pi raspbian ros kinetic workspace of pi(no. 38)
# Contact
* Author : Rajendra Singh
* Email : singh.raj1997@gmail.com
# File description
## refresh.sh
#### Run:    ./refresh.sh or . refresh.sh \
*It will source the workspace after buiding workspace or after creating new pkg.*
```
#!/bin/bash
source /opt/ros/kinetic/setup.bash
source /home/pi/ros_catkin_ws/devel/setup.bash
source /home/pi/ros_catkin_ws/devel_isolated/setup.bash
clear
```

* makefile
```
SHELL=/bin/bash
all:
	make run
run:
	catkin_make #catkin_make_isolated
	bash refresh.sh
```

* createpkg.sh
```
#!/bin/bash
cd src/
catkin create $1
cd ../
make
source refresh.sh
```

* tftree.sh
```
#!/bin/bash
rosrun rqt_tf_tree rqt_tf_tree
```

* printenv.sh
```
#!/bin/bash
printenv | grep -i ROS
```

* rosdep.sh
```
code
```

* rajendra.sh
```
#!/bin/bash
ssh rajendra@rajendra
```

* googleassistant.sh
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

# License
MIT License
Copyright (c) 2019 Rajendra Singh
