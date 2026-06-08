// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "saye_msgs/msg/detail/map__struct.h"
#include "saye_msgs/msg/detail/map__functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool nav2_msgs__msg__costmap_meta_data__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * nav2_msgs__msg__costmap_meta_data__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool nav2_msgs__msg__costmap__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * nav2_msgs__msg__costmap__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool nav_msgs__msg__occupancy_grid__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * nav_msgs__msg__occupancy_grid__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool nav_msgs__msg__map_meta_data__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * nav_msgs__msg__map_meta_data__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool nav_msgs__msg__path__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * nav_msgs__msg__path__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool saye_msgs__msg__map__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[23];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("saye_msgs.msg._map.Map", full_classname_dest, 22) == 0);
  }
  saye_msgs__msg__Map * ros_message = _ros_message;
  {  // costmap_meta_data
    PyObject * field = PyObject_GetAttrString(_pymsg, "costmap_meta_data");
    if (!field) {
      return false;
    }
    if (!nav2_msgs__msg__costmap_meta_data__convert_from_py(field, &ros_message->costmap_meta_data)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // costmap
    PyObject * field = PyObject_GetAttrString(_pymsg, "costmap");
    if (!field) {
      return false;
    }
    if (!nav2_msgs__msg__costmap__convert_from_py(field, &ros_message->costmap)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // occupancy_grid
    PyObject * field = PyObject_GetAttrString(_pymsg, "occupancy_grid");
    if (!field) {
      return false;
    }
    if (!nav_msgs__msg__occupancy_grid__convert_from_py(field, &ros_message->occupancy_grid)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // map_meta_data
    PyObject * field = PyObject_GetAttrString(_pymsg, "map_meta_data");
    if (!field) {
      return false;
    }
    if (!nav_msgs__msg__map_meta_data__convert_from_py(field, &ros_message->map_meta_data)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // path
    PyObject * field = PyObject_GetAttrString(_pymsg, "path");
    if (!field) {
      return false;
    }
    if (!nav_msgs__msg__path__convert_from_py(field, &ros_message->path)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * saye_msgs__msg__map__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Map */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("saye_msgs.msg._map");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Map");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  saye_msgs__msg__Map * ros_message = (saye_msgs__msg__Map *)raw_ros_message;
  {  // costmap_meta_data
    PyObject * field = NULL;
    field = nav2_msgs__msg__costmap_meta_data__convert_to_py(&ros_message->costmap_meta_data);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "costmap_meta_data", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // costmap
    PyObject * field = NULL;
    field = nav2_msgs__msg__costmap__convert_to_py(&ros_message->costmap);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "costmap", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // occupancy_grid
    PyObject * field = NULL;
    field = nav_msgs__msg__occupancy_grid__convert_to_py(&ros_message->occupancy_grid);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "occupancy_grid", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // map_meta_data
    PyObject * field = NULL;
    field = nav_msgs__msg__map_meta_data__convert_to_py(&ros_message->map_meta_data);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "map_meta_data", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // path
    PyObject * field = NULL;
    field = nav_msgs__msg__path__convert_to_py(&ros_message->path);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "path", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
