^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package rosconsole_bridge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.5.2 (2018-08-03)
------------------
* fix static destruction ordering issue on macOS (`#16 <https://github.com/ros/rosconsole_bridge/issues/16>`_)

0.5.1 (2017-11-05)
------------------
* fix use of deprecated logging functions (`#15 <https://github.com/ros/rosconsole_bridge/issues/15>`_, regression of 0.5.0)

0.5.0 (2017-10-25)
------------------
* replace usage of deprecated logging functions (`#14 <https://github.com/ros/rosconsole_bridge/issues/14>`_)

0.4.3 (2016-03-11)
------------------
* use catkin variables for install dirs (`#9 <https://github.com/ros/rosconsole_bridge/issues/9>`_)

0.4.2 (2014-07-18)
------------------
* update maintainers

0.4.1 (2014-06-25)
------------------
* update find_package for console bridge to reflect 3rdparty status (`#8 <https://github.com/ros/rosconsole_bridge/issues/8>`_)

0.4.0 (2014-06-24)
------------------
* rename variables within rosconsole macros (`ros/ros_comm#442 <https://github.com/ros/ros_comm/issues/442>`_)
* convert to use console bridge from upstream debian package (`ros/rosdistro#4633 <https://github.com/ros/rosdistro/issues/4633>`_)

0.3.4 (2014-02-15)
------------------
* Allows non-ros components to utilize the prefix functionality of log4j
* Contributors: Dave Coleman, Ioan A Sucan

0.3.3 (2013-08-21)
------------------
* fixing catkin as a buildtool dependency
* Contributors: Dirk Thomas, Tully Foote

0.3.2 (2013-04-12)
------------------
* changes due to renames in console_bridge
* Contributors: Ioan Sucan

0.3.1 (2013-03-13 21:24)
------------------------
* fix deps
* update e-mail address
* Contributors: Ioan Sucan

0.3.0 (2013-03-13 19:39)
------------------------

0.2.7 (2013-06-12)
------------------
* changes due to renames in console_bridge
* Create README.md
* Updated package xml to be more compliant to spec as well as adding maintainer
* Contributors: Ioan Sucan, Mirza Shah, isucan

0.2.6 (2012-12-10)
------------------
* update log level
* Fixing style issues in CMakeLists.txt
* Contributors: Ioan Sucan, William Woodall

0.2.5 (2012-12-05)
------------------
* Update cmake to pass along console_bridge
  Also changed it to depend on console_bridge
  like a catkin dependency.
* Added tag 0.2.4 for changeset e9f39dd361bf
* Contributors: Ioan Sucan, William Woodall, isucan

0.2.4 (2012-10-18)
------------------
* updates to package.xml
* Added tag 0.2.3 for changeset 63015a123bb7
* Contributors: Ioan Sucan, Tully Foote

0.2.3 (2012-10-06 23:24)
------------------------
* removing outdated install rule
* Added tag 0.2.2 for changeset 3fb270551aee
* Contributors: Tully Foote

0.2.2 (2012-10-06 18:49)
------------------------
* fixing depend tags
* Added tag 0.2.1 for changeset d4cfe2aea73d
* Contributors: Tully Foote

0.2.1 (2012-10-06 16:59)
------------------------
* converting to package.xml from stack.xml, and dropping manifest
* Added tag 0.2.0 for changeset 25da297e8ddb
* Contributors: Ioan Sucan, Tully Foote

0.2.0 (2012-09-02)
------------------
* update stack version
* patches for groovy
* Added tag fuerte for changeset f05a07a4dc8c
* Added tag 0.1.0 for changeset 119bd5db978d
* Contributors: Ioan Sucan

0.1.0 (2012-07-02 11:15)
------------------------
* first commit
* Contributors: Ioan Sucan
