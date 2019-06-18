SHELL=/bin/bash
all:
	make run
run:
	sudo ./src/catkin/bin/catkin_make_isolated
	bash refresh.sh
