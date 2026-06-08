// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from saye_msgs:srv/ShareMap.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "saye_msgs/srv/detail/share_map__rosidl_typesupport_introspection_c.h"
#include "saye_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "saye_msgs/srv/detail/share_map__functions.h"
#include "saye_msgs/srv/detail/share_map__struct.h"


// Include directives for member types
// Member `topic_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  saye_msgs__srv__ShareMap_Request__init(message_memory);
}

void saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_fini_function(void * message_memory)
{
  saye_msgs__srv__ShareMap_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_message_member_array[1] = {
  {
    "topic_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__srv__ShareMap_Request, topic_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_message_members = {
  "saye_msgs__srv",  // message namespace
  "ShareMap_Request",  // message name
  1,  // number of fields
  sizeof(saye_msgs__srv__ShareMap_Request),
  false,  // has_any_key_member_
  saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_message_member_array,  // message members
  saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_message_type_support_handle = {
  0,
  &saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_message_members,
  get_message_typesupport_handle_function,
  &saye_msgs__srv__ShareMap_Request__get_type_hash,
  &saye_msgs__srv__ShareMap_Request__get_type_description,
  &saye_msgs__srv__ShareMap_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_saye_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Request)() {
  if (!saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_message_type_support_handle.typesupport_identifier) {
    saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "saye_msgs/srv/detail/share_map__rosidl_typesupport_introspection_c.h"
// already included above
// #include "saye_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "saye_msgs/srv/detail/share_map__functions.h"
// already included above
// #include "saye_msgs/srv/detail/share_map__struct.h"


// Include directives for member types
// Member `custom_occupany_grid`
#include "nav_msgs/msg/occupancy_grid.h"
// Member `custom_occupany_grid`
#include "nav_msgs/msg/detail/occupancy_grid__rosidl_typesupport_introspection_c.h"
// Member `status_message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  saye_msgs__srv__ShareMap_Response__init(message_memory);
}

void saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_fini_function(void * message_memory)
{
  saye_msgs__srv__ShareMap_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_member_array[3] = {
  {
    "is_completed",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__srv__ShareMap_Response, is_completed),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "custom_occupany_grid",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__srv__ShareMap_Response, custom_occupany_grid),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "status_message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__srv__ShareMap_Response, status_message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_members = {
  "saye_msgs__srv",  // message namespace
  "ShareMap_Response",  // message name
  3,  // number of fields
  sizeof(saye_msgs__srv__ShareMap_Response),
  false,  // has_any_key_member_
  saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_member_array,  // message members
  saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_type_support_handle = {
  0,
  &saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_members,
  get_message_typesupport_handle_function,
  &saye_msgs__srv__ShareMap_Response__get_type_hash,
  &saye_msgs__srv__ShareMap_Response__get_type_description,
  &saye_msgs__srv__ShareMap_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_saye_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Response)() {
  saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nav_msgs, msg, OccupancyGrid)();
  if (!saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_type_support_handle.typesupport_identifier) {
    saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "saye_msgs/srv/detail/share_map__rosidl_typesupport_introspection_c.h"
// already included above
// #include "saye_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "saye_msgs/srv/detail/share_map__functions.h"
// already included above
// #include "saye_msgs/srv/detail/share_map__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "saye_msgs/srv/share_map.h"
// Member `request`
// Member `response`
// already included above
// #include "saye_msgs/srv/detail/share_map__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  saye_msgs__srv__ShareMap_Event__init(message_memory);
}

void saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_fini_function(void * message_memory)
{
  saye_msgs__srv__ShareMap_Event__fini(message_memory);
}

size_t saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__size_function__ShareMap_Event__request(
  const void * untyped_member)
{
  const saye_msgs__srv__ShareMap_Request__Sequence * member =
    (const saye_msgs__srv__ShareMap_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_const_function__ShareMap_Event__request(
  const void * untyped_member, size_t index)
{
  const saye_msgs__srv__ShareMap_Request__Sequence * member =
    (const saye_msgs__srv__ShareMap_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_function__ShareMap_Event__request(
  void * untyped_member, size_t index)
{
  saye_msgs__srv__ShareMap_Request__Sequence * member =
    (saye_msgs__srv__ShareMap_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__fetch_function__ShareMap_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const saye_msgs__srv__ShareMap_Request * item =
    ((const saye_msgs__srv__ShareMap_Request *)
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_const_function__ShareMap_Event__request(untyped_member, index));
  saye_msgs__srv__ShareMap_Request * value =
    (saye_msgs__srv__ShareMap_Request *)(untyped_value);
  *value = *item;
}

void saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__assign_function__ShareMap_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  saye_msgs__srv__ShareMap_Request * item =
    ((saye_msgs__srv__ShareMap_Request *)
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_function__ShareMap_Event__request(untyped_member, index));
  const saye_msgs__srv__ShareMap_Request * value =
    (const saye_msgs__srv__ShareMap_Request *)(untyped_value);
  *item = *value;
}

bool saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__resize_function__ShareMap_Event__request(
  void * untyped_member, size_t size)
{
  saye_msgs__srv__ShareMap_Request__Sequence * member =
    (saye_msgs__srv__ShareMap_Request__Sequence *)(untyped_member);
  saye_msgs__srv__ShareMap_Request__Sequence__fini(member);
  return saye_msgs__srv__ShareMap_Request__Sequence__init(member, size);
}

size_t saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__size_function__ShareMap_Event__response(
  const void * untyped_member)
{
  const saye_msgs__srv__ShareMap_Response__Sequence * member =
    (const saye_msgs__srv__ShareMap_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_const_function__ShareMap_Event__response(
  const void * untyped_member, size_t index)
{
  const saye_msgs__srv__ShareMap_Response__Sequence * member =
    (const saye_msgs__srv__ShareMap_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_function__ShareMap_Event__response(
  void * untyped_member, size_t index)
{
  saye_msgs__srv__ShareMap_Response__Sequence * member =
    (saye_msgs__srv__ShareMap_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__fetch_function__ShareMap_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const saye_msgs__srv__ShareMap_Response * item =
    ((const saye_msgs__srv__ShareMap_Response *)
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_const_function__ShareMap_Event__response(untyped_member, index));
  saye_msgs__srv__ShareMap_Response * value =
    (saye_msgs__srv__ShareMap_Response *)(untyped_value);
  *value = *item;
}

void saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__assign_function__ShareMap_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  saye_msgs__srv__ShareMap_Response * item =
    ((saye_msgs__srv__ShareMap_Response *)
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_function__ShareMap_Event__response(untyped_member, index));
  const saye_msgs__srv__ShareMap_Response * value =
    (const saye_msgs__srv__ShareMap_Response *)(untyped_value);
  *item = *value;
}

bool saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__resize_function__ShareMap_Event__response(
  void * untyped_member, size_t size)
{
  saye_msgs__srv__ShareMap_Response__Sequence * member =
    (saye_msgs__srv__ShareMap_Response__Sequence *)(untyped_member);
  saye_msgs__srv__ShareMap_Response__Sequence__fini(member);
  return saye_msgs__srv__ShareMap_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(saye_msgs__srv__ShareMap_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(saye_msgs__srv__ShareMap_Event, request),  // bytes offset in struct
    NULL,  // default value
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__size_function__ShareMap_Event__request,  // size() function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_const_function__ShareMap_Event__request,  // get_const(index) function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_function__ShareMap_Event__request,  // get(index) function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__fetch_function__ShareMap_Event__request,  // fetch(index, &value) function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__assign_function__ShareMap_Event__request,  // assign(index, value) function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__resize_function__ShareMap_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(saye_msgs__srv__ShareMap_Event, response),  // bytes offset in struct
    NULL,  // default value
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__size_function__ShareMap_Event__response,  // size() function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_const_function__ShareMap_Event__response,  // get_const(index) function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__get_function__ShareMap_Event__response,  // get(index) function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__fetch_function__ShareMap_Event__response,  // fetch(index, &value) function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__assign_function__ShareMap_Event__response,  // assign(index, value) function pointer
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__resize_function__ShareMap_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_members = {
  "saye_msgs__srv",  // message namespace
  "ShareMap_Event",  // message name
  3,  // number of fields
  sizeof(saye_msgs__srv__ShareMap_Event),
  false,  // has_any_key_member_
  saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_member_array,  // message members
  saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_type_support_handle = {
  0,
  &saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_members,
  get_message_typesupport_handle_function,
  &saye_msgs__srv__ShareMap_Event__get_type_hash,
  &saye_msgs__srv__ShareMap_Event__get_type_description,
  &saye_msgs__srv__ShareMap_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_saye_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Event)() {
  saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Request)();
  saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Response)();
  if (!saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_type_support_handle.typesupport_identifier) {
    saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "saye_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "saye_msgs/srv/detail/share_map__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_service_members = {
  "saye_msgs__srv",  // service namespace
  "ShareMap",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_Request_message_type_support_handle,
  NULL,  // response message
  // saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_Response_message_type_support_handle
  NULL  // event_message
  // saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_Response_message_type_support_handle
};


static rosidl_service_type_support_t saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_service_type_support_handle = {
  0,
  &saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_service_members,
  get_service_typesupport_handle_function,
  &saye_msgs__srv__ShareMap_Request__rosidl_typesupport_introspection_c__ShareMap_Request_message_type_support_handle,
  &saye_msgs__srv__ShareMap_Response__rosidl_typesupport_introspection_c__ShareMap_Response_message_type_support_handle,
  &saye_msgs__srv__ShareMap_Event__rosidl_typesupport_introspection_c__ShareMap_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    saye_msgs,
    srv,
    ShareMap
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    saye_msgs,
    srv,
    ShareMap
  ),
  &saye_msgs__srv__ShareMap__get_type_hash,
  &saye_msgs__srv__ShareMap__get_type_description,
  &saye_msgs__srv__ShareMap__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_saye_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap)(void) {
  if (!saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_service_type_support_handle.typesupport_identifier) {
    saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, saye_msgs, srv, ShareMap_Event)()->data;
  }

  return &saye_msgs__srv__detail__share_map__rosidl_typesupport_introspection_c__ShareMap_service_type_support_handle;
}
