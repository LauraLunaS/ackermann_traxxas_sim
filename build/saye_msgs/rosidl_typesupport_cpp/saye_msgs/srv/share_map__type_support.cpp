// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from saye_msgs:srv/ShareMap.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "saye_msgs/srv/detail/share_map__functions.h"
#include "saye_msgs/srv/detail/share_map__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace saye_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _ShareMap_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ShareMap_Request_type_support_ids_t;

static const _ShareMap_Request_type_support_ids_t _ShareMap_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ShareMap_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ShareMap_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ShareMap_Request_type_support_symbol_names_t _ShareMap_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, saye_msgs, srv, ShareMap_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, saye_msgs, srv, ShareMap_Request)),
  }
};

typedef struct _ShareMap_Request_type_support_data_t
{
  void * data[2];
} _ShareMap_Request_type_support_data_t;

static _ShareMap_Request_type_support_data_t _ShareMap_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ShareMap_Request_message_typesupport_map = {
  2,
  "saye_msgs",
  &_ShareMap_Request_message_typesupport_ids.typesupport_identifier[0],
  &_ShareMap_Request_message_typesupport_symbol_names.symbol_name[0],
  &_ShareMap_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ShareMap_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ShareMap_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &saye_msgs__srv__ShareMap_Request__get_type_hash,
  &saye_msgs__srv__ShareMap_Request__get_type_description,
  &saye_msgs__srv__ShareMap_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace saye_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<saye_msgs::srv::ShareMap_Request>()
{
  return &::saye_msgs::srv::rosidl_typesupport_cpp::ShareMap_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, saye_msgs, srv, ShareMap_Request)() {
  return get_message_type_support_handle<saye_msgs::srv::ShareMap_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "saye_msgs/srv/detail/share_map__functions.h"
// already included above
// #include "saye_msgs/srv/detail/share_map__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace saye_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _ShareMap_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ShareMap_Response_type_support_ids_t;

static const _ShareMap_Response_type_support_ids_t _ShareMap_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ShareMap_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ShareMap_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ShareMap_Response_type_support_symbol_names_t _ShareMap_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, saye_msgs, srv, ShareMap_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, saye_msgs, srv, ShareMap_Response)),
  }
};

typedef struct _ShareMap_Response_type_support_data_t
{
  void * data[2];
} _ShareMap_Response_type_support_data_t;

static _ShareMap_Response_type_support_data_t _ShareMap_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ShareMap_Response_message_typesupport_map = {
  2,
  "saye_msgs",
  &_ShareMap_Response_message_typesupport_ids.typesupport_identifier[0],
  &_ShareMap_Response_message_typesupport_symbol_names.symbol_name[0],
  &_ShareMap_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ShareMap_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ShareMap_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &saye_msgs__srv__ShareMap_Response__get_type_hash,
  &saye_msgs__srv__ShareMap_Response__get_type_description,
  &saye_msgs__srv__ShareMap_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace saye_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<saye_msgs::srv::ShareMap_Response>()
{
  return &::saye_msgs::srv::rosidl_typesupport_cpp::ShareMap_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, saye_msgs, srv, ShareMap_Response)() {
  return get_message_type_support_handle<saye_msgs::srv::ShareMap_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "saye_msgs/srv/detail/share_map__functions.h"
// already included above
// #include "saye_msgs/srv/detail/share_map__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace saye_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _ShareMap_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ShareMap_Event_type_support_ids_t;

static const _ShareMap_Event_type_support_ids_t _ShareMap_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ShareMap_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ShareMap_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ShareMap_Event_type_support_symbol_names_t _ShareMap_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, saye_msgs, srv, ShareMap_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, saye_msgs, srv, ShareMap_Event)),
  }
};

typedef struct _ShareMap_Event_type_support_data_t
{
  void * data[2];
} _ShareMap_Event_type_support_data_t;

static _ShareMap_Event_type_support_data_t _ShareMap_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ShareMap_Event_message_typesupport_map = {
  2,
  "saye_msgs",
  &_ShareMap_Event_message_typesupport_ids.typesupport_identifier[0],
  &_ShareMap_Event_message_typesupport_symbol_names.symbol_name[0],
  &_ShareMap_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ShareMap_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ShareMap_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &saye_msgs__srv__ShareMap_Event__get_type_hash,
  &saye_msgs__srv__ShareMap_Event__get_type_description,
  &saye_msgs__srv__ShareMap_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace saye_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<saye_msgs::srv::ShareMap_Event>()
{
  return &::saye_msgs::srv::rosidl_typesupport_cpp::ShareMap_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, saye_msgs, srv, ShareMap_Event)() {
  return get_message_type_support_handle<saye_msgs::srv::ShareMap_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "saye_msgs/srv/detail/share_map__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace saye_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _ShareMap_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ShareMap_type_support_ids_t;

static const _ShareMap_type_support_ids_t _ShareMap_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ShareMap_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ShareMap_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ShareMap_type_support_symbol_names_t _ShareMap_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, saye_msgs, srv, ShareMap)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, saye_msgs, srv, ShareMap)),
  }
};

typedef struct _ShareMap_type_support_data_t
{
  void * data[2];
} _ShareMap_type_support_data_t;

static _ShareMap_type_support_data_t _ShareMap_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ShareMap_service_typesupport_map = {
  2,
  "saye_msgs",
  &_ShareMap_service_typesupport_ids.typesupport_identifier[0],
  &_ShareMap_service_typesupport_symbol_names.symbol_name[0],
  &_ShareMap_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t ShareMap_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ShareMap_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<saye_msgs::srv::ShareMap_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<saye_msgs::srv::ShareMap_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<saye_msgs::srv::ShareMap_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<saye_msgs::srv::ShareMap>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<saye_msgs::srv::ShareMap>,
  &saye_msgs__srv__ShareMap__get_type_hash,
  &saye_msgs__srv__ShareMap__get_type_description,
  &saye_msgs__srv__ShareMap__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace saye_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<saye_msgs::srv::ShareMap>()
{
  return &::saye_msgs::srv::rosidl_typesupport_cpp::ShareMap_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, saye_msgs, srv, ShareMap)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<saye_msgs::srv::ShareMap>();
}

#ifdef __cplusplus
}
#endif
