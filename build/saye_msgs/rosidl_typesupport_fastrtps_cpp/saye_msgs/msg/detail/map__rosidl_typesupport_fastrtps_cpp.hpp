// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice

#ifndef SAYE_MSGS__MSG__DETAIL__MAP__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define SAYE_MSGS__MSG__DETAIL__MAP__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include <cstddef>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "saye_msgs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "saye_msgs/msg/detail/map__struct.hpp"

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

#include "fastcdr/Cdr.h"

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
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  saye_msgs::msg::Map & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
get_serialized_size(
  const saye_msgs::msg::Map & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
max_serialized_size_Map(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
cdr_serialize_key(
  const saye_msgs::msg::Map & ros_message,
  eprosima::fastcdr::Cdr &);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
get_serialized_size_key(
  const saye_msgs::msg::Map & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
max_serialized_size_key_Map(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace saye_msgs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_saye_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, saye_msgs, msg, Map)();

#ifdef __cplusplus
}
#endif

#endif  // SAYE_MSGS__MSG__DETAIL__MAP__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
