// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice
#include "saye_msgs/msg/detail/map__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `costmap_meta_data`
#include "nav2_msgs/msg/detail/costmap_meta_data__functions.h"
// Member `costmap`
#include "nav2_msgs/msg/detail/costmap__functions.h"
// Member `occupancy_grid`
#include "nav_msgs/msg/detail/occupancy_grid__functions.h"
// Member `map_meta_data`
#include "nav_msgs/msg/detail/map_meta_data__functions.h"
// Member `path`
#include "nav_msgs/msg/detail/path__functions.h"
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
saye_msgs__msg__Map__init(saye_msgs__msg__Map * msg)
{
  if (!msg) {
    return false;
  }
  // costmap_meta_data
  if (!nav2_msgs__msg__CostmapMetaData__init(&msg->costmap_meta_data)) {
    saye_msgs__msg__Map__fini(msg);
    return false;
  }
  // costmap
  if (!nav2_msgs__msg__Costmap__init(&msg->costmap)) {
    saye_msgs__msg__Map__fini(msg);
    return false;
  }
  // occupancy_grid
  if (!nav_msgs__msg__OccupancyGrid__init(&msg->occupancy_grid)) {
    saye_msgs__msg__Map__fini(msg);
    return false;
  }
  // map_meta_data
  if (!nav_msgs__msg__MapMetaData__init(&msg->map_meta_data)) {
    saye_msgs__msg__Map__fini(msg);
    return false;
  }
  // path
  if (!nav_msgs__msg__Path__init(&msg->path)) {
    saye_msgs__msg__Map__fini(msg);
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    saye_msgs__msg__Map__fini(msg);
    return false;
  }
  return true;
}

void
saye_msgs__msg__Map__fini(saye_msgs__msg__Map * msg)
{
  if (!msg) {
    return;
  }
  // costmap_meta_data
  nav2_msgs__msg__CostmapMetaData__fini(&msg->costmap_meta_data);
  // costmap
  nav2_msgs__msg__Costmap__fini(&msg->costmap);
  // occupancy_grid
  nav_msgs__msg__OccupancyGrid__fini(&msg->occupancy_grid);
  // map_meta_data
  nav_msgs__msg__MapMetaData__fini(&msg->map_meta_data);
  // path
  nav_msgs__msg__Path__fini(&msg->path);
  // header
  std_msgs__msg__Header__fini(&msg->header);
}

bool
saye_msgs__msg__Map__are_equal(const saye_msgs__msg__Map * lhs, const saye_msgs__msg__Map * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // costmap_meta_data
  if (!nav2_msgs__msg__CostmapMetaData__are_equal(
      &(lhs->costmap_meta_data), &(rhs->costmap_meta_data)))
  {
    return false;
  }
  // costmap
  if (!nav2_msgs__msg__Costmap__are_equal(
      &(lhs->costmap), &(rhs->costmap)))
  {
    return false;
  }
  // occupancy_grid
  if (!nav_msgs__msg__OccupancyGrid__are_equal(
      &(lhs->occupancy_grid), &(rhs->occupancy_grid)))
  {
    return false;
  }
  // map_meta_data
  if (!nav_msgs__msg__MapMetaData__are_equal(
      &(lhs->map_meta_data), &(rhs->map_meta_data)))
  {
    return false;
  }
  // path
  if (!nav_msgs__msg__Path__are_equal(
      &(lhs->path), &(rhs->path)))
  {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  return true;
}

bool
saye_msgs__msg__Map__copy(
  const saye_msgs__msg__Map * input,
  saye_msgs__msg__Map * output)
{
  if (!input || !output) {
    return false;
  }
  // costmap_meta_data
  if (!nav2_msgs__msg__CostmapMetaData__copy(
      &(input->costmap_meta_data), &(output->costmap_meta_data)))
  {
    return false;
  }
  // costmap
  if (!nav2_msgs__msg__Costmap__copy(
      &(input->costmap), &(output->costmap)))
  {
    return false;
  }
  // occupancy_grid
  if (!nav_msgs__msg__OccupancyGrid__copy(
      &(input->occupancy_grid), &(output->occupancy_grid)))
  {
    return false;
  }
  // map_meta_data
  if (!nav_msgs__msg__MapMetaData__copy(
      &(input->map_meta_data), &(output->map_meta_data)))
  {
    return false;
  }
  // path
  if (!nav_msgs__msg__Path__copy(
      &(input->path), &(output->path)))
  {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  return true;
}

saye_msgs__msg__Map *
saye_msgs__msg__Map__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__msg__Map * msg = (saye_msgs__msg__Map *)allocator.allocate(sizeof(saye_msgs__msg__Map), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(saye_msgs__msg__Map));
  bool success = saye_msgs__msg__Map__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
saye_msgs__msg__Map__destroy(saye_msgs__msg__Map * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    saye_msgs__msg__Map__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
saye_msgs__msg__Map__Sequence__init(saye_msgs__msg__Map__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__msg__Map * data = NULL;

  if (size) {
    data = (saye_msgs__msg__Map *)allocator.zero_allocate(size, sizeof(saye_msgs__msg__Map), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = saye_msgs__msg__Map__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        saye_msgs__msg__Map__fini(&data[i - 1]);
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
saye_msgs__msg__Map__Sequence__fini(saye_msgs__msg__Map__Sequence * array)
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
      saye_msgs__msg__Map__fini(&array->data[i]);
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

saye_msgs__msg__Map__Sequence *
saye_msgs__msg__Map__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  saye_msgs__msg__Map__Sequence * array = (saye_msgs__msg__Map__Sequence *)allocator.allocate(sizeof(saye_msgs__msg__Map__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = saye_msgs__msg__Map__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
saye_msgs__msg__Map__Sequence__destroy(saye_msgs__msg__Map__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    saye_msgs__msg__Map__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
saye_msgs__msg__Map__Sequence__are_equal(const saye_msgs__msg__Map__Sequence * lhs, const saye_msgs__msg__Map__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!saye_msgs__msg__Map__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
saye_msgs__msg__Map__Sequence__copy(
  const saye_msgs__msg__Map__Sequence * input,
  saye_msgs__msg__Map__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(saye_msgs__msg__Map);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    saye_msgs__msg__Map * data =
      (saye_msgs__msg__Map *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!saye_msgs__msg__Map__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          saye_msgs__msg__Map__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!saye_msgs__msg__Map__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
