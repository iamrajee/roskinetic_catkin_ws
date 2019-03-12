@[if DEVELSPACE]@
# bin and template dir variables in develspace
set(GENEUS_BIN "@(CMAKE_CURRENT_SOURCE_DIR)/scripts/gen_eus.py")
set(GENEUS_TEMPLATE_DIR "@(CMAKE_CURRENT_SOURCE_DIR)/scripts")
@[else]@
# bin and template dir variables in installspace
set(GENEUS_BIN "${geneus_DIR}/../../../@(CATKIN_PACKAGE_BIN_DESTINATION)/gen_eus.py")
set(GENEUS_TEMPLATE_DIR "${geneus_DIR}/..")
@[end if]@

# Generate .msg or .srv -> .l
# The generated .l files should be added ALL_GEN_OUTPUT_FILES_eus
macro(_generate_eus ARG_PKG ARG_MSG ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)
  file(MAKE_DIRECTORY ${ARG_GEN_OUTPUT_DIR})

  #Create input and output filenames
  get_filename_component(MSG_NAME ${ARG_MSG} NAME)
  get_filename_component(MSG_SHORT_NAME ${ARG_MSG} NAME_WE)

  set(MSG_GENERATED_NAME ${MSG_SHORT_NAME}.l)
  set(GEN_OUTPUT_FILE ${ARG_GEN_OUTPUT_DIR}/${MSG_GENERATED_NAME})

  assert(CATKIN_ENV)
  add_custom_command(OUTPUT ${GEN_OUTPUT_FILE}
    DEPENDS ${GENEUS_BIN} ${ARG_MSG} ${ARG_MSG_DEPS}
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENEUS_BIN} ${ARG_MSG}
    ${ARG_IFLAGS}
    -p ${ARG_PKG}
    -o ${ARG_GEN_OUTPUT_DIR}
    COMMENT "Generating EusLisp code from ${ARG_PKG}/${MSG_NAME}"
    )

  list(APPEND ALL_GEN_OUTPUT_FILES_eus ${GEN_OUTPUT_FILE})

endmacro()

#geneus uses the same program to generate srv and msg files, so call the same macro
macro(_generate_msg_eus ARG_PKG ARG_MSG ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)
  _generate_eus(${ARG_PKG} ${ARG_MSG} "${ARG_IFLAGS}" "${ARG_MSG_DEPS}" "${ARG_GEN_OUTPUT_DIR}/msg")
endmacro()

#geneus uses the same program to generate srv and msg files, so call the same macro
macro(_generate_srv_eus ARG_PKG ARG_SRV ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)
  _generate_eus(${ARG_PKG} ${ARG_SRV} "${ARG_IFLAGS}" "${ARG_MSG_DEPS}" "${ARG_GEN_OUTPUT_DIR}/srv")
endmacro()

macro(_generate_module_eus ARG_PKG ARG_GEN_OUTPUT_DIR ARG_GENERATED_FILES)
  file(MAKE_DIRECTORY ${ARG_GEN_OUTPUT_DIR})

  set(MODULE_GENERATED_NAME manifest.l)
  set(GEN_OUTPUT_FILE ${ARG_GEN_OUTPUT_DIR}/${MODULE_GENERATED_NAME})

  assert(CATKIN_ENV)
  add_custom_command(OUTPUT ${GEN_OUTPUT_FILE}
    DEPENDS ${GENEUS_BIN}
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENEUS_BIN}
    -m -o ${ARG_GEN_OUTPUT_DIR} ${ARG_PKG} ${ARG_DEPENDENCIES}
    COMMENT "Generating EusLisp manifest code for ${ARG_PKG}"
    )

  list(APPEND ALL_GEN_OUTPUT_FILES_eus ${GEN_OUTPUT_FILE})
endmacro()

set(roseus_INSTALL_DIR share/roseus)
set(geneus_INSTALL_DIR ${roseus_INSTALL_DIR}/ros)
