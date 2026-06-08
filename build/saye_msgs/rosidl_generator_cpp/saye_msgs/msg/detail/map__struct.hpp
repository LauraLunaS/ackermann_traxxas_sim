// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "saye_msgs/msg/map.hpp"


#ifndef SAYE_MSGS__MSG__DETAIL__MAP__STRUCT_HPP_
#define SAYE_MSGS__MSG__DETAIL__MAP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'costmap_meta_data'
#include "nav2_msgs/msg/detail/costmap_meta_data__struct.hpp"
// Member 'costmap'
#include "nav2_msgs/msg/detail/costmap__struct.hpp"
// Member 'occupancy_grid'
#include "nav_msgs/msg/detail/occupancy_grid__struct.hpp"
// Member 'map_meta_data'
#include "nav_msgs/msg/detail/map_meta_data__struct.hpp"
// Member 'path'
#include "nav_msgs/msg/detail/path__struct.hpp"
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__saye_msgs__msg__Map __attribute__((deprecated))
#else
# define DEPRECATED__saye_msgs__msg__Map __declspec(deprecated)
#endif

namespace saye_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Map_
{
  using Type = Map_<ContainerAllocator>;

  explicit Map_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : costmap_meta_data(_init),
    costmap(_init),
    occupancy_grid(_init),
    map_meta_data(_init),
    path(_init),
    header(_init)
  {
    (void)_init;
  }

  explicit Map_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : costmap_meta_data(_alloc, _init),
    costmap(_alloc, _init),
    occupancy_grid(_alloc, _init),
    map_meta_data(_alloc, _init),
    path(_alloc, _init),
    header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _costmap_meta_data_type =
    nav2_msgs::msg::CostmapMetaData_<ContainerAllocator>;
  _costmap_meta_data_type costmap_meta_data;
  using _costmap_type =
    nav2_msgs::msg::Costmap_<ContainerAllocator>;
  _costmap_type costmap;
  using _occupancy_grid_type =
    nav_msgs::msg::OccupancyGrid_<ContainerAllocator>;
  _occupancy_grid_type occupancy_grid;
  using _map_meta_data_type =
    nav_msgs::msg::MapMetaData_<ContainerAllocator>;
  _map_meta_data_type map_meta_data;
  using _path_type =
    nav_msgs::msg::Path_<ContainerAllocator>;
  _path_type path;
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;

  // setters for named parameter idiom
  Type & set__costmap_meta_data(
    const nav2_msgs::msg::CostmapMetaData_<ContainerAllocator> & _arg)
  {
    this->costmap_meta_data = _arg;
    return *this;
  }
  Type & set__costmap(
    const nav2_msgs::msg::Costmap_<ContainerAllocator> & _arg)
  {
    this->costmap = _arg;
    return *this;
  }
  Type & set__occupancy_grid(
    const nav_msgs::msg::OccupancyGrid_<ContainerAllocator> & _arg)
  {
    this->occupancy_grid = _arg;
    return *this;
  }
  Type & set__map_meta_data(
    const nav_msgs::msg::MapMetaData_<ContainerAllocator> & _arg)
  {
    this->map_meta_data = _arg;
    return *this;
  }
  Type & set__path(
    const nav_msgs::msg::Path_<ContainerAllocator> & _arg)
  {
    this->path = _arg;
    return *this;
  }
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    saye_msgs::msg::Map_<ContainerAllocator> *;
  using ConstRawPtr =
    const saye_msgs::msg::Map_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<saye_msgs::msg::Map_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<saye_msgs::msg::Map_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      saye_msgs::msg::Map_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<saye_msgs::msg::Map_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      saye_msgs::msg::Map_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<saye_msgs::msg::Map_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<saye_msgs::msg::Map_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<saye_msgs::msg::Map_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__saye_msgs__msg__Map
    std::shared_ptr<saye_msgs::msg::Map_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__saye_msgs__msg__Map
    std::shared_ptr<saye_msgs::msg::Map_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Map_ & other) const
  {
    if (this->costmap_meta_data != other.costmap_meta_data) {
      return false;
    }
    if (this->costmap != other.costmap) {
      return false;
    }
    if (this->occupancy_grid != other.occupancy_grid) {
      return false;
    }
    if (this->map_meta_data != other.map_meta_data) {
      return false;
    }
    if (this->path != other.path) {
      return false;
    }
    if (this->header != other.header) {
      return false;
    }
    return true;
  }
  bool operator!=(const Map_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Map_

// alias to use template instance with default allocator
using Map =
  saye_msgs::msg::Map_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace saye_msgs

#endif  // SAYE_MSGS__MSG__DETAIL__MAP__STRUCT_HPP_
