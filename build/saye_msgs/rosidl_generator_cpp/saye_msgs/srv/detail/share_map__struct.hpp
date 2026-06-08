// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from saye_msgs:srv/ShareMap.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "saye_msgs/srv/share_map.hpp"


#ifndef SAYE_MSGS__SRV__DETAIL__SHARE_MAP__STRUCT_HPP_
#define SAYE_MSGS__SRV__DETAIL__SHARE_MAP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__saye_msgs__srv__ShareMap_Request __attribute__((deprecated))
#else
# define DEPRECATED__saye_msgs__srv__ShareMap_Request __declspec(deprecated)
#endif

namespace saye_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ShareMap_Request_
{
  using Type = ShareMap_Request_<ContainerAllocator>;

  explicit ShareMap_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->topic_name = "";
    }
  }

  explicit ShareMap_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : topic_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->topic_name = "";
    }
  }

  // field types and members
  using _topic_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _topic_name_type topic_name;

  // setters for named parameter idiom
  Type & set__topic_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->topic_name = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    saye_msgs::srv::ShareMap_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const saye_msgs::srv::ShareMap_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<saye_msgs::srv::ShareMap_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<saye_msgs::srv::ShareMap_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      saye_msgs::srv::ShareMap_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<saye_msgs::srv::ShareMap_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      saye_msgs::srv::ShareMap_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<saye_msgs::srv::ShareMap_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<saye_msgs::srv::ShareMap_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<saye_msgs::srv::ShareMap_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__saye_msgs__srv__ShareMap_Request
    std::shared_ptr<saye_msgs::srv::ShareMap_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__saye_msgs__srv__ShareMap_Request
    std::shared_ptr<saye_msgs::srv::ShareMap_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ShareMap_Request_ & other) const
  {
    if (this->topic_name != other.topic_name) {
      return false;
    }
    return true;
  }
  bool operator!=(const ShareMap_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ShareMap_Request_

// alias to use template instance with default allocator
using ShareMap_Request =
  saye_msgs::srv::ShareMap_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace saye_msgs


// Include directives for member types
// Member 'custom_occupany_grid'
#include "nav_msgs/msg/detail/occupancy_grid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__saye_msgs__srv__ShareMap_Response __attribute__((deprecated))
#else
# define DEPRECATED__saye_msgs__srv__ShareMap_Response __declspec(deprecated)
#endif

namespace saye_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ShareMap_Response_
{
  using Type = ShareMap_Response_<ContainerAllocator>;

  explicit ShareMap_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : custom_occupany_grid(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_completed = false;
      this->status_message = "";
    }
  }

  explicit ShareMap_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : custom_occupany_grid(_alloc, _init),
    status_message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_completed = false;
      this->status_message = "";
    }
  }

  // field types and members
  using _is_completed_type =
    bool;
  _is_completed_type is_completed;
  using _custom_occupany_grid_type =
    nav_msgs::msg::OccupancyGrid_<ContainerAllocator>;
  _custom_occupany_grid_type custom_occupany_grid;
  using _status_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _status_message_type status_message;

  // setters for named parameter idiom
  Type & set__is_completed(
    const bool & _arg)
  {
    this->is_completed = _arg;
    return *this;
  }
  Type & set__custom_occupany_grid(
    const nav_msgs::msg::OccupancyGrid_<ContainerAllocator> & _arg)
  {
    this->custom_occupany_grid = _arg;
    return *this;
  }
  Type & set__status_message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->status_message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    saye_msgs::srv::ShareMap_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const saye_msgs::srv::ShareMap_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<saye_msgs::srv::ShareMap_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<saye_msgs::srv::ShareMap_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      saye_msgs::srv::ShareMap_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<saye_msgs::srv::ShareMap_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      saye_msgs::srv::ShareMap_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<saye_msgs::srv::ShareMap_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<saye_msgs::srv::ShareMap_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<saye_msgs::srv::ShareMap_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__saye_msgs__srv__ShareMap_Response
    std::shared_ptr<saye_msgs::srv::ShareMap_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__saye_msgs__srv__ShareMap_Response
    std::shared_ptr<saye_msgs::srv::ShareMap_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ShareMap_Response_ & other) const
  {
    if (this->is_completed != other.is_completed) {
      return false;
    }
    if (this->custom_occupany_grid != other.custom_occupany_grid) {
      return false;
    }
    if (this->status_message != other.status_message) {
      return false;
    }
    return true;
  }
  bool operator!=(const ShareMap_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ShareMap_Response_

// alias to use template instance with default allocator
using ShareMap_Response =
  saye_msgs::srv::ShareMap_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace saye_msgs


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__saye_msgs__srv__ShareMap_Event __attribute__((deprecated))
#else
# define DEPRECATED__saye_msgs__srv__ShareMap_Event __declspec(deprecated)
#endif

namespace saye_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ShareMap_Event_
{
  using Type = ShareMap_Event_<ContainerAllocator>;

  explicit ShareMap_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit ShareMap_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<saye_msgs::srv::ShareMap_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<saye_msgs::srv::ShareMap_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<saye_msgs::srv::ShareMap_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<saye_msgs::srv::ShareMap_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<saye_msgs::srv::ShareMap_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<saye_msgs::srv::ShareMap_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<saye_msgs::srv::ShareMap_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<saye_msgs::srv::ShareMap_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    saye_msgs::srv::ShareMap_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const saye_msgs::srv::ShareMap_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<saye_msgs::srv::ShareMap_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<saye_msgs::srv::ShareMap_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      saye_msgs::srv::ShareMap_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<saye_msgs::srv::ShareMap_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      saye_msgs::srv::ShareMap_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<saye_msgs::srv::ShareMap_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<saye_msgs::srv::ShareMap_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<saye_msgs::srv::ShareMap_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__saye_msgs__srv__ShareMap_Event
    std::shared_ptr<saye_msgs::srv::ShareMap_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__saye_msgs__srv__ShareMap_Event
    std::shared_ptr<saye_msgs::srv::ShareMap_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ShareMap_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const ShareMap_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ShareMap_Event_

// alias to use template instance with default allocator
using ShareMap_Event =
  saye_msgs::srv::ShareMap_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace saye_msgs

namespace saye_msgs
{

namespace srv
{

struct ShareMap
{
  using Request = saye_msgs::srv::ShareMap_Request;
  using Response = saye_msgs::srv::ShareMap_Response;
  using Event = saye_msgs::srv::ShareMap_Event;
};

}  // namespace srv

}  // namespace saye_msgs

#endif  // SAYE_MSGS__SRV__DETAIL__SHARE_MAP__STRUCT_HPP_
