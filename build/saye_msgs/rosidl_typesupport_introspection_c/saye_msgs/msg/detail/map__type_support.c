// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "saye_msgs/msg/detail/map__rosidl_typesupport_introspection_c.h"
#include "saye_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "saye_msgs/msg/detail/map__functions.h"
#include "saye_msgs/msg/detail/map__struct.h"


// Include directives for member types
// Member `costmap_meta_data`
#include "nav2_msgs/msg/costmap_meta_data.h"
// Member `costmap_meta_data`
#include "nav2_msgs/msg/detail/costmap_meta_data__rosidl_typesupport_introspection_c.h"
// Member `costmap`
#include "nav2_msgs/msg/costmap.h"
// Member `costmap`
#include "nav2_msgs/msg/detail/costmap__rosidl_typesupport_introspection_c.h"
// Member `occupancy_grid`
#include "nav_msgs/msg/occupancy_grid.h"
// Member `occupancy_grid`
#include "nav_msgs/msg/detail/occupancy_grid__rosidl_typesupport_introspection_c.h"
// Member `map_meta_data`
#include "nav_msgs/msg/map_meta_data.h"
// Member `map_meta_data`
#include "nav_msgs/msg/detail/map_meta_data__rosidl_typesupport_introspection_c.h"
// Member `path`
#include "nav_msgs/msg/path.h"
// Member `path`
#include "nav_msgs/msg/detail/path__rosidl_typesupport_introspection_c.h"
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  saye_msgs__msg__Map__init(message_memory);
}

void saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_fini_function(void * message_memory)
{
  saye_msgs__msg__Map__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_member_array[6] = {
  {
    "costmap_meta_data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__msg__Map, costmap_meta_data),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "costmap",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__msg__Map, costmap),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "occupancy_grid",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__msg__Map, occupancy_grid),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "map_meta_data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__msg__Map, map_meta_data),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "path",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__msg__Map, path),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__msg__Map, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_members = {
  "saye_msgs__msg",  // message namespace
  "Map",  // message name
  6,  // number of fields
  sizeof(saye_msgs__msg__Map),
  false,  // has_any_key_member_
  saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_member_array,  // message members
  saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_init_function,  // function to initialize message memory (memory has to be allocated)
  saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_type_support_handle = {
  0,
  &saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_members,
  get_message_typesupport_handle_function,
  &saye_msgs__msg__Map__get_type_hash,
  &saye_msgs__msg__Map__get_type_description,
  &saye_msgs__msg__Map__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_saye_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, msg, Map)() {
  saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nav2_msgs, msg, CostmapMetaData)();
  saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nav2_msgs, msg, Costmap)();
  saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nav_msgs, msg, OccupancyGrid)();
  saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nav_msgs, msg, MapMetaData)();
  saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nav_msgs, msg, Path)();
  saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_type_support_handle.typesupport_identifier) {
    saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &saye_msgs__msg__Map__rosidl_typesupport_introspection_c__Map_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
