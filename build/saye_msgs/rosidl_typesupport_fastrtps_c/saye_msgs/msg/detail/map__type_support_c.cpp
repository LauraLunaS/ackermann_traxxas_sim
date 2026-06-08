// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice
#include "saye_msgs/msg/detail/map__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "saye_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "saye_msgs/msg/detail/map__struct.h"
#include "saye_msgs/msg/detail/map__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "nav2_msgs/msg/detail/costmap__functions.h"  // costmap
#include "nav2_msgs/msg/detail/costmap_meta_data__functions.h"  // costmap_meta_data
#include "nav_msgs/msg/detail/map_meta_data__functions.h"  // map_meta_data
#include "nav_msgs/msg/detail/occupancy_grid__functions.h"  // occupancy_grid
#include "nav_msgs/msg/detail/path__functions.h"  // path
#include "std_msgs/msg/detail/header__functions.h"  // header

// forward declare type support functions

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_nav2_msgs__msg__Costmap(
  const nav2_msgs__msg__Costmap * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_deserialize_nav2_msgs__msg__Costmap(
  eprosima::fastcdr::Cdr & cdr,
  nav2_msgs__msg__Costmap * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_nav2_msgs__msg__Costmap(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_nav2_msgs__msg__Costmap(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_key_nav2_msgs__msg__Costmap(
  const nav2_msgs__msg__Costmap * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_key_nav2_msgs__msg__Costmap(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_key_nav2_msgs__msg__Costmap(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nav2_msgs, msg, Costmap)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_nav2_msgs__msg__CostmapMetaData(
  const nav2_msgs__msg__CostmapMetaData * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_deserialize_nav2_msgs__msg__CostmapMetaData(
  eprosima::fastcdr::Cdr & cdr,
  nav2_msgs__msg__CostmapMetaData * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_nav2_msgs__msg__CostmapMetaData(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_nav2_msgs__msg__CostmapMetaData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_key_nav2_msgs__msg__CostmapMetaData(
  const nav2_msgs__msg__CostmapMetaData * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_key_nav2_msgs__msg__CostmapMetaData(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_key_nav2_msgs__msg__CostmapMetaData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nav2_msgs, msg, CostmapMetaData)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_nav_msgs__msg__MapMetaData(
  const nav_msgs__msg__MapMetaData * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_deserialize_nav_msgs__msg__MapMetaData(
  eprosima::fastcdr::Cdr & cdr,
  nav_msgs__msg__MapMetaData * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_nav_msgs__msg__MapMetaData(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_nav_msgs__msg__MapMetaData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_key_nav_msgs__msg__MapMetaData(
  const nav_msgs__msg__MapMetaData * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_key_nav_msgs__msg__MapMetaData(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_key_nav_msgs__msg__MapMetaData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nav_msgs, msg, MapMetaData)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_nav_msgs__msg__OccupancyGrid(
  const nav_msgs__msg__OccupancyGrid * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_deserialize_nav_msgs__msg__OccupancyGrid(
  eprosima::fastcdr::Cdr & cdr,
  nav_msgs__msg__OccupancyGrid * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_nav_msgs__msg__OccupancyGrid(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_nav_msgs__msg__OccupancyGrid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_key_nav_msgs__msg__OccupancyGrid(
  const nav_msgs__msg__OccupancyGrid * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_key_nav_msgs__msg__OccupancyGrid(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_key_nav_msgs__msg__OccupancyGrid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nav_msgs, msg, OccupancyGrid)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_nav_msgs__msg__Path(
  const nav_msgs__msg__Path * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_deserialize_nav_msgs__msg__Path(
  eprosima::fastcdr::Cdr & cdr,
  nav_msgs__msg__Path * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_nav_msgs__msg__Path(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_nav_msgs__msg__Path(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_key_nav_msgs__msg__Path(
  const nav_msgs__msg__Path * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_key_nav_msgs__msg__Path(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_key_nav_msgs__msg__Path(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nav_msgs, msg, Path)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_std_msgs__msg__Header(
  const std_msgs__msg__Header * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_deserialize_std_msgs__msg__Header(
  eprosima::fastcdr::Cdr & cdr,
  std_msgs__msg__Header * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
bool cdr_serialize_key_std_msgs__msg__Header(
  const std_msgs__msg__Header * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t get_serialized_size_key_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
size_t max_serialized_size_key_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_saye_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Header)();


using _Map__ros_msg_type = saye_msgs__msg__Map;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_saye_msgs
bool cdr_serialize_saye_msgs__msg__Map(
  const saye_msgs__msg__Map * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: costmap_meta_data
  {
    cdr_serialize_nav2_msgs__msg__CostmapMetaData(
      &ros_message->costmap_meta_data, cdr);
  }

  // Field name: costmap
  {
    cdr_serialize_nav2_msgs__msg__Costmap(
      &ros_message->costmap, cdr);
  }

  // Field name: occupancy_grid
  {
    cdr_serialize_nav_msgs__msg__OccupancyGrid(
      &ros_message->occupancy_grid, cdr);
  }

  // Field name: map_meta_data
  {
    cdr_serialize_nav_msgs__msg__MapMetaData(
      &ros_message->map_meta_data, cdr);
  }

  // Field name: path
  {
    cdr_serialize_nav_msgs__msg__Path(
      &ros_message->path, cdr);
  }

  // Field name: header
  {
    cdr_serialize_std_msgs__msg__Header(
      &ros_message->header, cdr);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_saye_msgs
bool cdr_deserialize_saye_msgs__msg__Map(
  eprosima::fastcdr::Cdr & cdr,
  saye_msgs__msg__Map * ros_message)
{
  // Field name: costmap_meta_data
  {
    cdr_deserialize_nav2_msgs__msg__CostmapMetaData(cdr, &ros_message->costmap_meta_data);
  }

  // Field name: costmap
  {
    cdr_deserialize_nav2_msgs__msg__Costmap(cdr, &ros_message->costmap);
  }

  // Field name: occupancy_grid
  {
    cdr_deserialize_nav_msgs__msg__OccupancyGrid(cdr, &ros_message->occupancy_grid);
  }

  // Field name: map_meta_data
  {
    cdr_deserialize_nav_msgs__msg__MapMetaData(cdr, &ros_message->map_meta_data);
  }

  // Field name: path
  {
    cdr_deserialize_nav_msgs__msg__Path(cdr, &ros_message->path);
  }

  // Field name: header
  {
    cdr_deserialize_std_msgs__msg__Header(cdr, &ros_message->header);
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_saye_msgs
size_t get_serialized_size_saye_msgs__msg__Map(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Map__ros_msg_type * ros_message = static_cast<const _Map__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: costmap_meta_data
  current_alignment += get_serialized_size_nav2_msgs__msg__CostmapMetaData(
    &(ros_message->costmap_meta_data), current_alignment);

  // Field name: costmap
  current_alignment += get_serialized_size_nav2_msgs__msg__Costmap(
    &(ros_message->costmap), current_alignment);

  // Field name: occupancy_grid
  current_alignment += get_serialized_size_nav_msgs__msg__OccupancyGrid(
    &(ros_message->occupancy_grid), current_alignment);

  // Field name: map_meta_data
  current_alignment += get_serialized_size_nav_msgs__msg__MapMetaData(
    &(ros_message->map_meta_data), current_alignment);

  // Field name: path
  current_alignment += get_serialized_size_nav_msgs__msg__Path(
    &(ros_message->path), current_alignment);

  // Field name: header
  current_alignment += get_serialized_size_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_saye_msgs
size_t max_serialized_size_saye_msgs__msg__Map(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: costmap_meta_data
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_nav2_msgs__msg__CostmapMetaData(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: costmap
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_nav2_msgs__msg__Costmap(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: occupancy_grid
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_nav_msgs__msg__OccupancyGrid(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: map_meta_data
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_nav_msgs__msg__MapMetaData(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: path
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_nav_msgs__msg__Path(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = saye_msgs__msg__Map;
    is_plain =
      (
      offsetof(DataType, header) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_saye_msgs
bool cdr_serialize_key_saye_msgs__msg__Map(
  const saye_msgs__msg__Map * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: costmap_meta_data
  {
    cdr_serialize_key_nav2_msgs__msg__CostmapMetaData(
      &ros_message->costmap_meta_data, cdr);
  }

  // Field name: costmap
  {
    cdr_serialize_key_nav2_msgs__msg__Costmap(
      &ros_message->costmap, cdr);
  }

  // Field name: occupancy_grid
  {
    cdr_serialize_key_nav_msgs__msg__OccupancyGrid(
      &ros_message->occupancy_grid, cdr);
  }

  // Field name: map_meta_data
  {
    cdr_serialize_key_nav_msgs__msg__MapMetaData(
      &ros_message->map_meta_data, cdr);
  }

  // Field name: path
  {
    cdr_serialize_key_nav_msgs__msg__Path(
      &ros_message->path, cdr);
  }

  // Field name: header
  {
    cdr_serialize_key_std_msgs__msg__Header(
      &ros_message->header, cdr);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_saye_msgs
size_t get_serialized_size_key_saye_msgs__msg__Map(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Map__ros_msg_type * ros_message = static_cast<const _Map__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: costmap_meta_data
  current_alignment += get_serialized_size_key_nav2_msgs__msg__CostmapMetaData(
    &(ros_message->costmap_meta_data), current_alignment);

  // Field name: costmap
  current_alignment += get_serialized_size_key_nav2_msgs__msg__Costmap(
    &(ros_message->costmap), current_alignment);

  // Field name: occupancy_grid
  current_alignment += get_serialized_size_key_nav_msgs__msg__OccupancyGrid(
    &(ros_message->occupancy_grid), current_alignment);

  // Field name: map_meta_data
  current_alignment += get_serialized_size_key_nav_msgs__msg__MapMetaData(
    &(ros_message->map_meta_data), current_alignment);

  // Field name: path
  current_alignment += get_serialized_size_key_nav_msgs__msg__Path(
    &(ros_message->path), current_alignment);

  // Field name: header
  current_alignment += get_serialized_size_key_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_saye_msgs
size_t max_serialized_size_key_saye_msgs__msg__Map(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: costmap_meta_data
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_nav2_msgs__msg__CostmapMetaData(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: costmap
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_nav2_msgs__msg__Costmap(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: occupancy_grid
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_nav_msgs__msg__OccupancyGrid(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: map_meta_data
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_nav_msgs__msg__MapMetaData(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: path
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_nav_msgs__msg__Path(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = saye_msgs__msg__Map;
    is_plain =
      (
      offsetof(DataType, header) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _Map__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const saye_msgs__msg__Map * ros_message = static_cast<const saye_msgs__msg__Map *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_saye_msgs__msg__Map(ros_message, cdr);
}

static bool _Map__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  saye_msgs__msg__Map * ros_message = static_cast<saye_msgs__msg__Map *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_saye_msgs__msg__Map(cdr, ros_message);
}

static uint32_t _Map__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_saye_msgs__msg__Map(
      untyped_ros_message, 0));
}

static size_t _Map__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_saye_msgs__msg__Map(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Map = {
  "saye_msgs::msg",
  "Map",
  _Map__cdr_serialize,
  _Map__cdr_deserialize,
  _Map__get_serialized_size,
  _Map__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _Map__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Map,
  get_message_typesupport_handle_function,
  &saye_msgs__msg__Map__get_type_hash,
  &saye_msgs__msg__Map__get_type_description,
  &saye_msgs__msg__Map__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, saye_msgs, msg, Map)() {
  return &_Map__type_support;
}

#if defined(__cplusplus)
}
#endif
