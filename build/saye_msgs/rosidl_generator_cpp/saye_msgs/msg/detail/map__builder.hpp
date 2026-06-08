// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "saye_msgs/msg/map.hpp"


#ifndef SAYE_MSGS__MSG__DETAIL__MAP__BUILDER_HPP_
#define SAYE_MSGS__MSG__DETAIL__MAP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "saye_msgs/msg/detail/map__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace saye_msgs
{

namespace msg
{

namespace builder
{

class Init_Map_header
{
public:
  explicit Init_Map_header(::saye_msgs::msg::Map & msg)
  : msg_(msg)
  {}
  ::saye_msgs::msg::Map header(::saye_msgs::msg::Map::_header_type arg)
  {
    msg_.header = std::move(arg);
    return std::move(msg_);
  }

private:
  ::saye_msgs::msg::Map msg_;
};

class Init_Map_path
{
public:
  explicit Init_Map_path(::saye_msgs::msg::Map & msg)
  : msg_(msg)
  {}
  Init_Map_header path(::saye_msgs::msg::Map::_path_type arg)
  {
    msg_.path = std::move(arg);
    return Init_Map_header(msg_);
  }

private:
  ::saye_msgs::msg::Map msg_;
};

class Init_Map_map_meta_data
{
public:
  explicit Init_Map_map_meta_data(::saye_msgs::msg::Map & msg)
  : msg_(msg)
  {}
  Init_Map_path map_meta_data(::saye_msgs::msg::Map::_map_meta_data_type arg)
  {
    msg_.map_meta_data = std::move(arg);
    return Init_Map_path(msg_);
  }

private:
  ::saye_msgs::msg::Map msg_;
};

class Init_Map_occupancy_grid
{
public:
  explicit Init_Map_occupancy_grid(::saye_msgs::msg::Map & msg)
  : msg_(msg)
  {}
  Init_Map_map_meta_data occupancy_grid(::saye_msgs::msg::Map::_occupancy_grid_type arg)
  {
    msg_.occupancy_grid = std::move(arg);
    return Init_Map_map_meta_data(msg_);
  }

private:
  ::saye_msgs::msg::Map msg_;
};

class Init_Map_costmap
{
public:
  explicit Init_Map_costmap(::saye_msgs::msg::Map & msg)
  : msg_(msg)
  {}
  Init_Map_occupancy_grid costmap(::saye_msgs::msg::Map::_costmap_type arg)
  {
    msg_.costmap = std::move(arg);
    return Init_Map_occupancy_grid(msg_);
  }

private:
  ::saye_msgs::msg::Map msg_;
};

class Init_Map_costmap_meta_data
{
public:
  Init_Map_costmap_meta_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Map_costmap costmap_meta_data(::saye_msgs::msg::Map::_costmap_meta_data_type arg)
  {
    msg_.costmap_meta_data = std::move(arg);
    return Init_Map_costmap(msg_);
  }

private:
  ::saye_msgs::msg::Map msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::saye_msgs::msg::Map>()
{
  return saye_msgs::msg::builder::Init_Map_costmap_meta_data();
}

}  // namespace saye_msgs

#endif  // SAYE_MSGS__MSG__DETAIL__MAP__BUILDER_HPP_
