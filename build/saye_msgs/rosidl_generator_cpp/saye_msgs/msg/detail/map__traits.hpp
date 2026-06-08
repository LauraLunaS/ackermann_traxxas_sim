// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "saye_msgs/msg/map.hpp"


#ifndef SAYE_MSGS__MSG__DETAIL__MAP__TRAITS_HPP_
#define SAYE_MSGS__MSG__DETAIL__MAP__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "saye_msgs/msg/detail/map__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'costmap_meta_data'
#include "nav2_msgs/msg/detail/costmap_meta_data__traits.hpp"
// Member 'costmap'
#include "nav2_msgs/msg/detail/costmap__traits.hpp"
// Member 'occupancy_grid'
#include "nav_msgs/msg/detail/occupancy_grid__traits.hpp"
// Member 'map_meta_data'
#include "nav_msgs/msg/detail/map_meta_data__traits.hpp"
// Member 'path'
#include "nav_msgs/msg/detail/path__traits.hpp"
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace saye_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Map & msg,
  std::ostream & out)
{
  out << "{";
  // member: costmap_meta_data
  {
    out << "costmap_meta_data: ";
    to_flow_style_yaml(msg.costmap_meta_data, out);
    out << ", ";
  }

  // member: costmap
  {
    out << "costmap: ";
    to_flow_style_yaml(msg.costmap, out);
    out << ", ";
  }

  // member: occupancy_grid
  {
    out << "occupancy_grid: ";
    to_flow_style_yaml(msg.occupancy_grid, out);
    out << ", ";
  }

  // member: map_meta_data
  {
    out << "map_meta_data: ";
    to_flow_style_yaml(msg.map_meta_data, out);
    out << ", ";
  }

  // member: path
  {
    out << "path: ";
    to_flow_style_yaml(msg.path, out);
    out << ", ";
  }

  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Map & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: costmap_meta_data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "costmap_meta_data:\n";
    to_block_style_yaml(msg.costmap_meta_data, out, indentation + 2);
  }

  // member: costmap
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "costmap:\n";
    to_block_style_yaml(msg.costmap, out, indentation + 2);
  }

  // member: occupancy_grid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "occupancy_grid:\n";
    to_block_style_yaml(msg.occupancy_grid, out, indentation + 2);
  }

  // member: map_meta_data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "map_meta_data:\n";
    to_block_style_yaml(msg.map_meta_data, out, indentation + 2);
  }

  // member: path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "path:\n";
    to_block_style_yaml(msg.path, out, indentation + 2);
  }

  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Map & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace saye_msgs

namespace rosidl_generator_traits
{

[[deprecated("use saye_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const saye_msgs::msg::Map & msg,
  std::ostream & out, size_t indentation = 0)
{
  saye_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use saye_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const saye_msgs::msg::Map & msg)
{
  return saye_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<saye_msgs::msg::Map>()
{
  return "saye_msgs::msg::Map";
}

template<>
inline const char * name<saye_msgs::msg::Map>()
{
  return "saye_msgs/msg/Map";
}

template<>
struct has_fixed_size<saye_msgs::msg::Map>
  : std::integral_constant<bool, has_fixed_size<nav2_msgs::msg::Costmap>::value && has_fixed_size<nav2_msgs::msg::CostmapMetaData>::value && has_fixed_size<nav_msgs::msg::MapMetaData>::value && has_fixed_size<nav_msgs::msg::OccupancyGrid>::value && has_fixed_size<nav_msgs::msg::Path>::value && has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<saye_msgs::msg::Map>
  : std::integral_constant<bool, has_bounded_size<nav2_msgs::msg::Costmap>::value && has_bounded_size<nav2_msgs::msg::CostmapMetaData>::value && has_bounded_size<nav_msgs::msg::MapMetaData>::value && has_bounded_size<nav_msgs::msg::OccupancyGrid>::value && has_bounded_size<nav_msgs::msg::Path>::value && has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<saye_msgs::msg::Map>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SAYE_MSGS__MSG__DETAIL__MAP__TRAITS_HPP_
