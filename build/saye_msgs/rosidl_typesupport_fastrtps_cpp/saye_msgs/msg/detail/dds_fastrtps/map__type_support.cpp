// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice
#include "saye_msgs/msg/detail/map__rosidl_typesupport_fastrtps_cpp.hpp"
#include "saye_msgs/msg/detail/map__functions.h"
#include "saye_msgs/msg/detail/map__struct.hpp"

#include <cstddef>
#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions
namespace nav2_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const nav2_msgs::msg::CostmapMetaData &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  nav2_msgs::msg::CostmapMetaData &);
size_t get_serialized_size(
  const nav2_msgs::msg::CostmapMetaData &,
  size_t current_alignment);
size_t
max_serialized_size_CostmapMetaData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
bool cdr_serialize_key(
  const nav2_msgs::msg::CostmapMetaData &,
  eprosima::fastcdr::Cdr &);
size_t get_serialized_size_key(
  const nav2_msgs::msg::CostmapMetaData &,
  size_t current_alignment);
size_t
max_serialized_size_key_CostmapMetaData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace nav2_msgs

namespace nav2_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const nav2_msgs::msg::Costmap &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  nav2_msgs::msg::Costmap &);
size_t get_serialized_size(
  const nav2_msgs::msg::Costmap &,
  size_t current_alignment);
size_t
max_serialized_size_Costmap(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
bool cdr_serialize_key(
  const nav2_msgs::msg::Costmap &,
  eprosima::fastcdr::Cdr &);
size_t get_serialized_size_key(
  const nav2_msgs::msg::Costmap &,
  size_t current_alignment);
size_t
max_serialized_size_key_Costmap(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace nav2_msgs

namespace nav_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const nav_msgs::msg::OccupancyGrid &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  nav_msgs::msg::OccupancyGrid &);
size_t get_serialized_size(
  const nav_msgs::msg::OccupancyGrid &,
  size_t current_alignment);
size_t
max_serialized_size_OccupancyGrid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
bool cdr_serialize_key(
  const nav_msgs::msg::OccupancyGrid &,
  eprosima::fastcdr::Cdr &);
size_t get_serialized_size_key(
  const nav_msgs::msg::OccupancyGrid &,
  size_t current_alignment);
size_t
max_serialized_size_key_OccupancyGrid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace nav_msgs

namespace nav_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const nav_msgs::msg::MapMetaData &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  nav_msgs::msg::MapMetaData &);
size_t get_serialized_size(
  const nav_msgs::msg::MapMetaData &,
  size_t current_alignment);
size_t
max_serialized_size_MapMetaData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
bool cdr_serialize_key(
  const nav_msgs::msg::MapMetaData &,
  eprosima::fastcdr::Cdr &);
size_t get_serialized_size_key(
  const nav_msgs::msg::MapMetaData &,
  size_t current_alignment);
size_t
max_serialized_size_key_MapMetaData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace nav_msgs

namespace nav_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const nav_msgs::msg::Path &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  nav_msgs::msg::Path &);
size_t get_serialized_size(
  const nav_msgs::msg::Path &,
  size_t current_alignment);
size_t
max_serialized_size_Path(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
bool cdr_serialize_key(
  const nav_msgs::msg::Path &,
  eprosima::fastcdr::Cdr &);
size_t get_serialized_size_key(
  const nav_msgs::msg::Path &,
  size_t current_alignment);
size_t
max_serialized_size_key_Path(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace nav_msgs

namespace std_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const std_msgs::msg::Header &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  std_msgs::msg::Header &);
size_t get_serialized_size(
  const std_msgs::msg::Header &,
  size_t current_alignment);
size_t
max_serialized_size_Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
bool cdr_serialize_key(
  const std_msgs::msg::Header &,
  eprosima::fastcdr::Cdr &);
size_t get_serialized_size_key(
  const std_msgs::msg::Header &,
  size_t current_alignment);
size_t
max_serialized_size_key_Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace std_msgs


namespace saye_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{


bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
cdr_serialize(
  const saye_msgs::msg::Map & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: costmap_meta_data
  nav2_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.costmap_meta_data,
    cdr);

  // Member: costmap
  nav2_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.costmap,
    cdr);

  // Member: occupancy_grid
  nav_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.occupancy_grid,
    cdr);

  // Member: map_meta_data
  nav_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.map_meta_data,
    cdr);

  // Member: path
  nav_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.path,
    cdr);

  // Member: header
  std_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.header,
    cdr);

  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  saye_msgs::msg::Map & ros_message)
{
  // Member: costmap_meta_data
  nav2_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.costmap_meta_data);

  // Member: costmap
  nav2_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.costmap);

  // Member: occupancy_grid
  nav_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.occupancy_grid);

  // Member: map_meta_data
  nav_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.map_meta_data);

  // Member: path
  nav_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.path);

  // Member: header
  std_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.header);

  return true;
}  // NOLINT(readability/fn_size)


size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
get_serialized_size(
  const saye_msgs::msg::Map & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: costmap_meta_data
  current_alignment +=
    nav2_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.costmap_meta_data, current_alignment);

  // Member: costmap
  current_alignment +=
    nav2_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.costmap, current_alignment);

  // Member: occupancy_grid
  current_alignment +=
    nav_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.occupancy_grid, current_alignment);

  // Member: map_meta_data
  current_alignment +=
    nav_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.map_meta_data, current_alignment);

  // Member: path
  current_alignment +=
    nav_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.path, current_alignment);

  // Member: header
  current_alignment +=
    std_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.header, current_alignment);

  return current_alignment - initial_alignment;
}


size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
max_serialized_size_Map(
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

  // Member: costmap_meta_data
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav2_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_CostmapMetaData(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // Member: costmap
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav2_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_Costmap(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // Member: occupancy_grid
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_OccupancyGrid(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // Member: map_meta_data
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_MapMetaData(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // Member: path
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_Path(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // Member: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        std_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_Header(
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
    using DataType = saye_msgs::msg::Map;
    is_plain =
      (
      offsetof(DataType, header) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
cdr_serialize_key(
  const saye_msgs::msg::Map & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: costmap_meta_data
  nav2_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize_key(
    ros_message.costmap_meta_data,
    cdr);

  // Member: costmap
  nav2_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize_key(
    ros_message.costmap,
    cdr);

  // Member: occupancy_grid
  nav_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize_key(
    ros_message.occupancy_grid,
    cdr);

  // Member: map_meta_data
  nav_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize_key(
    ros_message.map_meta_data,
    cdr);

  // Member: path
  nav_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize_key(
    ros_message.path,
    cdr);

  // Member: header
  std_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize_key(
    ros_message.header,
    cdr);

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
get_serialized_size_key(
  const saye_msgs::msg::Map & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: costmap_meta_data
  current_alignment +=
    nav2_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size_key(
    ros_message.costmap_meta_data, current_alignment);

  // Member: costmap
  current_alignment +=
    nav2_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size_key(
    ros_message.costmap, current_alignment);

  // Member: occupancy_grid
  current_alignment +=
    nav_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size_key(
    ros_message.occupancy_grid, current_alignment);

  // Member: map_meta_data
  current_alignment +=
    nav_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size_key(
    ros_message.map_meta_data, current_alignment);

  // Member: path
  current_alignment +=
    nav_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size_key(
    ros_message.path, current_alignment);

  // Member: header
  current_alignment +=
    std_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size_key(
    ros_message.header, current_alignment);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
max_serialized_size_key_Map(
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

  // Member: costmap_meta_data
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav2_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_key_CostmapMetaData(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: costmap
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav2_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_key_Costmap(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: occupancy_grid
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_key_OccupancyGrid(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: map_meta_data
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_key_MapMetaData(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: path
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        nav_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_key_Path(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        std_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_key_Header(
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
    using DataType = saye_msgs::msg::Map;
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
  auto typed_message =
    static_cast<const saye_msgs::msg::Map *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Map__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<saye_msgs::msg::Map *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Map__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const saye_msgs::msg::Map *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Map__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Map(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Map__callbacks = {
  "saye_msgs::msg",
  "Map",
  _Map__cdr_serialize,
  _Map__cdr_deserialize,
  _Map__get_serialized_size,
  _Map__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _Map__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Map__callbacks,
  get_message_typesupport_handle_function,
  &saye_msgs__msg__Map__get_type_hash,
  &saye_msgs__msg__Map__get_type_description,
  &saye_msgs__msg__Map__get_type_description_sources,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace saye_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_saye_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<saye_msgs::msg::Map>()
{
  return &saye_msgs::msg::typesupport_fastrtps_cpp::_Map__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, saye_msgs, msg, Map)() {
  return &saye_msgs::msg::typesupport_fastrtps_cpp::_Map__handle;
}

#ifdef __cplusplus
}
#endif
