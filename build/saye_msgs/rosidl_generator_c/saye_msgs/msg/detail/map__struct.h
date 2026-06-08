// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "saye_msgs/msg/map.h"


#ifndef SAYE_MSGS__MSG__DETAIL__MAP__STRUCT_H_
#define SAYE_MSGS__MSG__DETAIL__MAP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'costmap_meta_data'
#include "nav2_msgs/msg/detail/costmap_meta_data__struct.h"
// Member 'costmap'
#include "nav2_msgs/msg/detail/costmap__struct.h"
// Member 'occupancy_grid'
#include "nav_msgs/msg/detail/occupancy_grid__struct.h"
// Member 'map_meta_data'
#include "nav_msgs/msg/detail/map_meta_data__struct.h"
// Member 'path'
#include "nav_msgs/msg/detail/path__struct.h"
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/Map in the package saye_msgs.
typedef struct saye_msgs__msg__Map
{
  nav2_msgs__msg__CostmapMetaData costmap_meta_data;
  nav2_msgs__msg__Costmap costmap;
  nav_msgs__msg__OccupancyGrid occupancy_grid;
  nav_msgs__msg__MapMetaData map_meta_data;
  nav_msgs__msg__Path path;
  std_msgs__msg__Header header;
} saye_msgs__msg__Map;

// Struct for a sequence of saye_msgs__msg__Map.
typedef struct saye_msgs__msg__Map__Sequence
{
  saye_msgs__msg__Map * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} saye_msgs__msg__Map__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SAYE_MSGS__MSG__DETAIL__MAP__STRUCT_H_
