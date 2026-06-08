// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from saye_msgs:srv/ShareMap.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "saye_msgs/srv/share_map.hpp"


#ifndef SAYE_MSGS__SRV__DETAIL__SHARE_MAP__BUILDER_HPP_
#define SAYE_MSGS__SRV__DETAIL__SHARE_MAP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "saye_msgs/srv/detail/share_map__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace saye_msgs
{

namespace srv
{

namespace builder
{

class Init_ShareMap_Request_topic_name
{
public:
  Init_ShareMap_Request_topic_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::saye_msgs::srv::ShareMap_Request topic_name(::saye_msgs::srv::ShareMap_Request::_topic_name_type arg)
  {
    msg_.topic_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::saye_msgs::srv::ShareMap_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::saye_msgs::srv::ShareMap_Request>()
{
  return saye_msgs::srv::builder::Init_ShareMap_Request_topic_name();
}

}  // namespace saye_msgs


namespace saye_msgs
{

namespace srv
{

namespace builder
{

class Init_ShareMap_Response_status_message
{
public:
  explicit Init_ShareMap_Response_status_message(::saye_msgs::srv::ShareMap_Response & msg)
  : msg_(msg)
  {}
  ::saye_msgs::srv::ShareMap_Response status_message(::saye_msgs::srv::ShareMap_Response::_status_message_type arg)
  {
    msg_.status_message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::saye_msgs::srv::ShareMap_Response msg_;
};

class Init_ShareMap_Response_custom_occupany_grid
{
public:
  explicit Init_ShareMap_Response_custom_occupany_grid(::saye_msgs::srv::ShareMap_Response & msg)
  : msg_(msg)
  {}
  Init_ShareMap_Response_status_message custom_occupany_grid(::saye_msgs::srv::ShareMap_Response::_custom_occupany_grid_type arg)
  {
    msg_.custom_occupany_grid = std::move(arg);
    return Init_ShareMap_Response_status_message(msg_);
  }

private:
  ::saye_msgs::srv::ShareMap_Response msg_;
};

class Init_ShareMap_Response_is_completed
{
public:
  Init_ShareMap_Response_is_completed()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ShareMap_Response_custom_occupany_grid is_completed(::saye_msgs::srv::ShareMap_Response::_is_completed_type arg)
  {
    msg_.is_completed = std::move(arg);
    return Init_ShareMap_Response_custom_occupany_grid(msg_);
  }

private:
  ::saye_msgs::srv::ShareMap_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::saye_msgs::srv::ShareMap_Response>()
{
  return saye_msgs::srv::builder::Init_ShareMap_Response_is_completed();
}

}  // namespace saye_msgs


namespace saye_msgs
{

namespace srv
{

namespace builder
{

class Init_ShareMap_Event_response
{
public:
  explicit Init_ShareMap_Event_response(::saye_msgs::srv::ShareMap_Event & msg)
  : msg_(msg)
  {}
  ::saye_msgs::srv::ShareMap_Event response(::saye_msgs::srv::ShareMap_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::saye_msgs::srv::ShareMap_Event msg_;
};

class Init_ShareMap_Event_request
{
public:
  explicit Init_ShareMap_Event_request(::saye_msgs::srv::ShareMap_Event & msg)
  : msg_(msg)
  {}
  Init_ShareMap_Event_response request(::saye_msgs::srv::ShareMap_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_ShareMap_Event_response(msg_);
  }

private:
  ::saye_msgs::srv::ShareMap_Event msg_;
};

class Init_ShareMap_Event_info
{
public:
  Init_ShareMap_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ShareMap_Event_request info(::saye_msgs::srv::ShareMap_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_ShareMap_Event_request(msg_);
  }

private:
  ::saye_msgs::srv::ShareMap_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::saye_msgs::srv::ShareMap_Event>()
{
  return saye_msgs::srv::builder::Init_ShareMap_Event_info();
}

}  // namespace saye_msgs

#endif  // SAYE_MSGS__SRV__DETAIL__SHARE_MAP__BUILDER_HPP_
