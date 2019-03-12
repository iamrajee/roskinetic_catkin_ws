^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package gennodejs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.0.1 (2017-2-16)
------------------
* Fix an issue uncovered in checking fixed size message fields
* Contributors: Chris Smith

2.0.0 (2017-1-18)
------------------
* The following changes make 2.0 incompatible with JavaScript
messages objects generated in gennodejs 1.x
* Bundled updates
  * Optionally accept object when constructing messages
  * Add md5sum for Service
  * Updates to generated code to use pre-allocated buffers
  * Generated code relies on external npm package for
  base serialization, deserialization, finding other
  message packages
  * Handle ros_msg_utils npm package rename
  * Incorrect argument, push array serialization to ros_msg_utils
  * Remove unused get message fixed size method
* Contributors: Chris Smith, Ian McMahon

1.0.3 (2016-5-18)
------------------
* Removed extraneous base file installs
* Revert install space fix that re-used base js files per package
* Added install space fix that copies base js files per package
* Contributors: Ian McMahon, Rob Linsalata

1.0.2 (2016-5-18)
------------------
* Fixed gennodejs file deployment in install space
* Fixed a python3 incompatibility in generate.py
* Contributors: Chris Smith, Ian McMahon, Maarten de Vries

1.0.1 (2016-4-27)
-----------
* Package name-switch from genjs to gennodejs based on feedback
* When deserializing, creates an instance of the message
  rather than using json.
* Update genjs for install
  -No longer includes hardcoded paths in generated message files
  -Actually install stuff
* Contributors: Chris Smith, Ian McMahon, chris-smith

1.0.0 (2016-4-19)
------------------
* Initial Release
* ROS JS Message Generation
* Builds automatically with catkin
* Include support for ROS Services
* Constants, Msg instances
  -generated msgs are now classes
  -msgs have constants included
* Contributors: Chris Smith, Ian McMahon
