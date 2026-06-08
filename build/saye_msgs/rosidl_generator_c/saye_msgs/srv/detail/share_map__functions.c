// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from saye_msgs:srv/ShareMap.idl
// generated code does not contain a copyright notice
#include "saye_msgs/srv/detail/share_map__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `topic_name`
#include "rosidl_runtime_c/string_functions.h"

bool
saye_msgs__srv__ShareMap_Request__init(saye_msgs__srv__ShareMap_Request * msg)
{
  if (!msg) {
    return false;
  }
  // topic_name
  if (!rosidl_runtime_c__String__init(&msg->topic_name)) {
    saye_msgs__srv__ShareMap_Request__fini(msg);
    return false;
  }
  return true;
}

void
saye_msgs__srv__ShareMap_Request__fini(saye_msgs__srv__ShareMap_Request * msg)
{
  if (!msg) {
    return;
  }
  // topic_name
  rosidl_runtime_c__String__fini(&msg->topic_name);
}

bool
saye_msgs__srv__ShareMap_Request__are_equal(const saye_msgs__srv__ShareMap_Request * lhs, const saye_msgs__srv__ShareMap_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // topic_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->topic_name), &(rhs->topic_name)))
  {
    return false;
  }
  return true;
}

bool
saye_msgs__srv__ShareMap_Request__copy(
  const saye_msgs__srv__ShareMap_Request * input,
  saye_msgs__srv__ShareMap_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // topic_name
  if (!rosidl_runtime_c__String__copy(
      &(input->topic_name), &(output->topic_name)))
  {
    return false;
  }
  return true;
}

saye_msgs__srv__ShareMap_Request *
saye_msgs__srv__ShareMap_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__srv__ShareMap_Request * msg = (saye_msgs__srv__ShareMap_Request *)allocator.allocate(sizeof(saye_msgs__srv__ShareMap_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(saye_msgs__srv__ShareMap_Request));
  bool success = saye_msgs__srv__ShareMap_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
saye_msgs__srv__ShareMap_Request__destroy(saye_msgs__srv__ShareMap_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    saye_msgs__srv__ShareMap_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
saye_msgs__srv__ShareMap_Request__Sequence__init(saye_msgs__srv__ShareMap_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__srv__ShareMap_Request * data = NULL;

  if (size) {
    data = (saye_msgs__srv__ShareMap_Request *)allocator.zero_allocate(size, sizeof(saye_msgs__srv__ShareMap_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = saye_msgs__srv__ShareMap_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        saye_msgs__srv__ShareMap_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
saye_msgs__srv__ShareMap_Request__Sequence__fini(saye_msgs__srv__ShareMap_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      saye_msgs__srv__ShareMap_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

saye_msgs__srv__ShareMap_Request__Sequence *
saye_msgs__srv__ShareMap_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__srv__ShareMap_Request__Sequence * array = (saye_msgs__srv__ShareMap_Request__Sequence *)allocator.allocate(sizeof(saye_msgs__srv__ShareMap_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = saye_msgs__srv__ShareMap_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
saye_msgs__srv__ShareMap_Request__Sequence__destroy(saye_msgs__srv__ShareMap_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    saye_msgs__srv__ShareMap_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
saye_msgs__srv__ShareMap_Request__Sequence__are_equal(const saye_msgs__srv__ShareMap_Request__Sequence * lhs, const saye_msgs__srv__ShareMap_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!saye_msgs__srv__ShareMap_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
saye_msgs__srv__ShareMap_Request__Sequence__copy(
  const saye_msgs__srv__ShareMap_Request__Sequence * input,
  saye_msgs__srv__ShareMap_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(saye_msgs__srv__ShareMap_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    saye_msgs__srv__ShareMap_Request * data =
      (saye_msgs__srv__ShareMap_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!saye_msgs__srv__ShareMap_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          saye_msgs__srv__ShareMap_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!saye_msgs__srv__ShareMap_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `custom_occupany_grid`
#include "nav_msgs/msg/detail/occupancy_grid__functions.h"
// Member `status_message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
saye_msgs__srv__ShareMap_Response__init(saye_msgs__srv__ShareMap_Response * msg)
{
  if (!msg) {
    return false;
  }
  // is_completed
  // custom_occupany_grid
  if (!nav_msgs__msg__OccupancyGrid__init(&msg->custom_occupany_grid)) {
    saye_msgs__srv__ShareMap_Response__fini(msg);
    return false;
  }
  // status_message
  if (!rosidl_runtime_c__String__init(&msg->status_message)) {
    saye_msgs__srv__ShareMap_Response__fini(msg);
    return false;
  }
  return true;
}

void
saye_msgs__srv__ShareMap_Response__fini(saye_msgs__srv__ShareMap_Response * msg)
{
  if (!msg) {
    return;
  }
  // is_completed
  // custom_occupany_grid
  nav_msgs__msg__OccupancyGrid__fini(&msg->custom_occupany_grid);
  // status_message
  rosidl_runtime_c__String__fini(&msg->status_message);
}

bool
saye_msgs__srv__ShareMap_Response__are_equal(const saye_msgs__srv__ShareMap_Response * lhs, const saye_msgs__srv__ShareMap_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // is_completed
  if (lhs->is_completed != rhs->is_completed) {
    return false;
  }
  // custom_occupany_grid
  if (!nav_msgs__msg__OccupancyGrid__are_equal(
      &(lhs->custom_occupany_grid), &(rhs->custom_occupany_grid)))
  {
    return false;
  }
  // status_message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->status_message), &(rhs->status_message)))
  {
    return false;
  }
  return true;
}

bool
saye_msgs__srv__ShareMap_Response__copy(
  const saye_msgs__srv__ShareMap_Response * input,
  saye_msgs__srv__ShareMap_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // is_completed
  output->is_completed = input->is_completed;
  // custom_occupany_grid
  if (!nav_msgs__msg__OccupancyGrid__copy(
      &(input->custom_occupany_grid), &(output->custom_occupany_grid)))
  {
    return false;
  }
  // status_message
  if (!rosidl_runtime_c__String__copy(
      &(input->status_message), &(output->status_message)))
  {
    return false;
  }
  return true;
}

saye_msgs__srv__ShareMap_Response *
saye_msgs__srv__ShareMap_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__srv__ShareMap_Response * msg = (saye_msgs__srv__ShareMap_Response *)allocator.allocate(sizeof(saye_msgs__srv__ShareMap_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(saye_msgs__srv__ShareMap_Response));
  bool success = saye_msgs__srv__ShareMap_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
saye_msgs__srv__ShareMap_Response__destroy(saye_msgs__srv__ShareMap_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    saye_msgs__srv__ShareMap_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
saye_msgs__srv__ShareMap_Response__Sequence__init(saye_msgs__srv__ShareMap_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__srv__ShareMap_Response * data = NULL;

  if (size) {
    data = (saye_msgs__srv__ShareMap_Response *)allocator.zero_allocate(size, sizeof(saye_msgs__srv__ShareMap_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = saye_msgs__srv__ShareMap_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        saye_msgs__srv__ShareMap_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
saye_msgs__srv__ShareMap_Response__Sequence__fini(saye_msgs__srv__ShareMap_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      saye_msgs__srv__ShareMap_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

saye_msgs__srv__ShareMap_Response__Sequence *
saye_msgs__srv__ShareMap_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__srv__ShareMap_Response__Sequence * array = (saye_msgs__srv__ShareMap_Response__Sequence *)allocator.allocate(sizeof(saye_msgs__srv__ShareMap_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = saye_msgs__srv__ShareMap_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
saye_msgs__srv__ShareMap_Response__Sequence__destroy(saye_msgs__srv__ShareMap_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    saye_msgs__srv__ShareMap_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
saye_msgs__srv__ShareMap_Response__Sequence__are_equal(const saye_msgs__srv__ShareMap_Response__Sequence * lhs, const saye_msgs__srv__ShareMap_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!saye_msgs__srv__ShareMap_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
saye_msgs__srv__ShareMap_Response__Sequence__copy(
  const saye_msgs__srv__ShareMap_Response__Sequence * input,
  saye_msgs__srv__ShareMap_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(saye_msgs__srv__ShareMap_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    saye_msgs__srv__ShareMap_Response * data =
      (saye_msgs__srv__ShareMap_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!saye_msgs__srv__ShareMap_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          saye_msgs__srv__ShareMap_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!saye_msgs__srv__ShareMap_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "saye_msgs/srv/detail/share_map__functions.h"

bool
saye_msgs__srv__ShareMap_Event__init(saye_msgs__srv__ShareMap_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    saye_msgs__srv__ShareMap_Event__fini(msg);
    return false;
  }
  // request
  if (!saye_msgs__srv__ShareMap_Request__Sequence__init(&msg->request, 0)) {
    saye_msgs__srv__ShareMap_Event__fini(msg);
    return false;
  }
  // response
  if (!saye_msgs__srv__ShareMap_Response__Sequence__init(&msg->response, 0)) {
    saye_msgs__srv__ShareMap_Event__fini(msg);
    return false;
  }
  return true;
}

void
saye_msgs__srv__ShareMap_Event__fini(saye_msgs__srv__ShareMap_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  saye_msgs__srv__ShareMap_Request__Sequence__fini(&msg->request);
  // response
  saye_msgs__srv__ShareMap_Response__Sequence__fini(&msg->response);
}

bool
saye_msgs__srv__ShareMap_Event__are_equal(const saye_msgs__srv__ShareMap_Event * lhs, const saye_msgs__srv__ShareMap_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!saye_msgs__srv__ShareMap_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!saye_msgs__srv__ShareMap_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
saye_msgs__srv__ShareMap_Event__copy(
  const saye_msgs__srv__ShareMap_Event * input,
  saye_msgs__srv__ShareMap_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!saye_msgs__srv__ShareMap_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!saye_msgs__srv__ShareMap_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

saye_msgs__srv__ShareMap_Event *
saye_msgs__srv__ShareMap_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__srv__ShareMap_Event * msg = (saye_msgs__srv__ShareMap_Event *)allocator.allocate(sizeof(saye_msgs__srv__ShareMap_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(saye_msgs__srv__ShareMap_Event));
  bool success = saye_msgs__srv__ShareMap_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
saye_msgs__srv__ShareMap_Event__destroy(saye_msgs__srv__ShareMap_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    saye_msgs__srv__ShareMap_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
saye_msgs__srv__ShareMap_Event__Sequence__init(saye_msgs__srv__ShareMap_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__srv__ShareMap_Event * data = NULL;

  if (size) {
    data = (saye_msgs__srv__ShareMap_Event *)allocator.zero_allocate(size, sizeof(saye_msgs__srv__ShareMap_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = saye_msgs__srv__ShareMap_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        saye_msgs__srv__ShareMap_Event__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
saye_msgs__srv__ShareMap_Event__Sequence__fini(saye_msgs__srv__ShareMap_Event__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      saye_msgs__srv__ShareMap_Event__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

saye_msgs__srv__ShareMap_Event__Sequence *
saye_msgs__srv__ShareMap_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__srv__ShareMap_Event__Sequence * array = (saye_msgs__srv__ShareMap_Event__Sequence *)allocator.allocate(sizeof(saye_msgs__srv__ShareMap_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = saye_msgs__srv__ShareMap_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
saye_msgs__srv__ShareMap_Event__Sequence__destroy(saye_msgs__srv__ShareMap_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    saye_msgs__srv__ShareMap_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
saye_msgs__srv__ShareMap_Event__Sequence__are_equal(const saye_msgs__srv__ShareMap_Event__Sequence * lhs, const saye_msgs__srv__ShareMap_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!saye_msgs__srv__ShareMap_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
saye_msgs__srv__ShareMap_Event__Sequence__copy(
  const saye_msgs__srv__ShareMap_Event__Sequence * input,
  saye_msgs__srv__ShareMap_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(saye_msgs__srv__ShareMap_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    saye_msgs__srv__ShareMap_Event * data =
      (saye_msgs__srv__ShareMap_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!saye_msgs__srv__ShareMap_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          saye_msgs__srv__ShareMap_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!saye_msgs__srv__ShareMap_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
