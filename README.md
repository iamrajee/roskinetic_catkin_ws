# ROS Kinetic Workspace for Raspbian OS (Source build) 
<!---(Raspi#38)--->
## Table of content
- [Maintainer](https://github.com/iamrajee/roskinetic_catkin_ws#maintainer)
- [Installation](https://github.com/iamrajee/roskinetic_catkin_ws#installation)
- [Package description](https://github.com/iamrajee/roskinetic_catkin_ws#package-description)
- [Helper scripts](https://github.com/iamrajee/roskinetic_catkin_ws#helper-scripts)
- [Team](https://github.com/iamrajee/roskinetic_catkin_ws#team)
- [Contributing](https://github.com/iamrajee/roskinetic_catkin_ws#contributing)
- [FAQ](https://github.com/iamrajee/roskinetic_catkin_ws#faq)
- [Support](https://github.com/iamrajee/roskinetic_catkin_ws#support)
- [License](https://github.com/iamrajee/roskinetic_catkin_ws#license)
- [Acknowledgments](https://github.com/iamrajee/roskinetic_catkin_ws#acknowledgments)
<!--- - [xyz](link) --->

---

## Maintainer
* Name : Rajendra Singh
* Email  : singh.raj1997@gmail.com
* Web    : https://iamrajee.github.io/
* LinkedIn    : https://www.linkedin.com/in/rajendra-singh-6b0b3a13a/
---

## Installation

- All the `code` required to get started
- #### Prerequisite
	- You should have ROS 1 kinectic build from source on your raspberry pi(raspbian OS).
	- All ROS dependency are satisfied.

- #### Clone

	```
	git clone https://github.com/iamrajee/roskinetic_catkin_ws.git
	```

- #### Setup
	```
	cd roskinetic_catkin_ws/
	./refresh.sh
	make
	```
---


## Package description
* ## [firstpkg](src/firstpkg)
	first pkg to create simple talker and listener.*

	Terminal 1:
	```
	$ roscore
	$ rosrun firstpkg talker.py
	```
	Terminal 2:
	```
	$ rosrun firstpkg listen.py
	```


* ## [manualcontrol](src/manualcontrol)
	![RAWBOT 2.0](demogif/RAWBOT.gif)\
	See full video [here](https://youtu.be/wrBw4yES4Eo).
	*In this pkg is create for a robot name RAWBOT,which is surveling robot.*

* ## [manualcontrol_slave](src/manualcontrol_slave)
	*This pkg is similar to manualcontrol with some more functionality and modification, and it is meant to be used on ROS Master which is used as Slave in system on robots*

---

# Helper Scripts

* ## refresh.sh
	```
	#!/bin/bash
	source /opt/ros/kinetic/setup.bash
	source ~/ros_catkin_ws/devel/setup.bash
	source ~/ros_catkin_ws/devel_isolated/setup.bash
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
	*It will create new package . Run it as `./createpkg.sh newpkg_name`*

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
	sudo rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y
	```
	*It will install dependencies of all pkg in the workspace . Run it in workspace as `./rosdep.sh`*

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

---
<br/><br/>
## Team

> Or Contributors/supporters/mentors/guides who helped me out in these projects.
<!---
| <a href="https://github.com/MuskaanMaheshwari" target="_blank">**Muskaan Maheshwari**</a> | <a href="https://www.linkedin.com/in/sachin-rustagi-882b55145/" target="_blank">**Sachin Rustagi**</a> | <a href="https://www.linkedin.com/in/s-m-rafi-911442130/" target="_blank">**S M Rafi**</a> |
| :---: |:---:| :---:|
--->
| <a href="https://github.com/MuskaanMaheshwari" target="_blank">**Muskaan Maheshwari**</a> | <a href="https://www.linkedin.com/in/sachin-rustagi-882b55145/" target="_blank">**Sachin Rustagi**</a> | <a href="https://www.linkedin.com/in/amin-swamiprasad-pkd-17732b152/" target="_blank">**Swami Prasad**</a> |
| :---: |:---:| :---:|
| ![](https://avatars0.githubusercontent.com/u/18076234?s=200&v=3) | ![](https://avatars0.githubusercontent.com/u/2555224?s=200&v=3) | ![](https://avatars0.githubusercontent.com/u/917816?s=200&v=3)  |


<!--- 
https://avatars3.githubusercontent.com/u/38295159?s=200&v=3
| <a href="http://github.com/fvcproductions" target="_blank">`github.com/fvcproductions`</a> | <a href="http://github.com/fvcproductions" target="_blank">`github.com/fvcproductions`</a> | <a href="http://github.com/fvcproductions" target="_blank">`github.com/fvcproductions`</a> |
https://www.linkedin.com/in/renjithdevi/
https://www.linkedin.com/in/sachin-rustagi-882b55145/
https://www.linkedin.com/in/amin-swamiprasad-pkd-17732b152/
sources:-
https://stackoverflow.com/questions/52063556/add-image-to-github-readme-md-from-google-drive
https://stackoverflow.com/questions/14494747/add-images-to-readme-md-on-github
https://gist.github.com/uupaa/f77d2bcf4dc7a294d109
https://github.com/jgm/pandoc/issues/2554
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
https://gist.github.com/PurpleBooth/109311bb0361f32d87a2
https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46#file-samplereadme-md
https://github.com/icholy/ttygif
--->


---
<br/><br/>
## Contributing

> To get started...

### Step 1

- **Option 1**
    - 🍴 Fork this repo!

- **Option 2**
    - 👯 Clone this repo to your local machine using `https://github.com/iamrajee/roskinetic_catkin_ws.git`

### Step 2

- **HACK AWAY!** 🔨🔨🔨

### Step 3

- 🔃 Create a new pull request using <a href="https://github.com/iamrajee/roskinetic_catkin_ws/compare/" target="_blank">`https://github.com/iamrajee/roskinetic_catkin_ws/compare/`</a>.
---
<br/><br/>
## FAQ

- **I ran into xyz issue while running above package, what do I do?**
    - Simply contact me!

---

## Support

Reach out to me at one of the following places!

- Website: <a href="https://iamrajee.github.io/" target="_blank">`iamrajee.github.io/`</a>
- Twitter: <a href="https://twitter.com/i_am_rajee" target="_blank">`@i_am_rajee`</a>
- Email  : singh.raj1997@gmail.com
- LinkedIn: at <a href="https://www.linkedin.com/in/rajendra-singh-6b0b3a13a/" target="_blank">`@Rajendra Singh`</a>
---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright (c) 2019 Rajendra Singh.
---

## Acknowledgments

* Hat tip to anyone whose code was used and thanks to everyone who inspired and supported me in this project.
