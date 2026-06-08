// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from saye_msgs:msg/Map.idl
// generated code does not contain a copyright notice

#include "saye_msgs/msg/detail/map__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_saye_msgs
const rosidl_type_hash_t *
saye_msgs__msg__Map__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xe7, 0xf2, 0x5e, 0xbd, 0x7d, 0x55, 0xbd, 0xfd,
      0x5e, 0xb9, 0x5b, 0xe3, 0xc8, 0x28, 0xe7, 0xd8,
      0xcb, 0x0c, 0x1e, 0x14, 0x97, 0x15, 0x12, 0xb7,
      0xf2, 0xf5, 0xaa, 0x9f, 0x49, 0x06, 0x34, 0x6f,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "geometry_msgs/msg/detail/pose_stamped__functions.h"
#include "nav2_msgs/msg/detail/costmap__functions.h"
#include "geometry_msgs/msg/detail/quaternion__functions.h"
#include "geometry_msgs/msg/detail/pose__functions.h"
#include "nav2_msgs/msg/detail/costmap_meta_data__functions.h"
#include "std_msgs/msg/detail/header__functions.h"
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "nav_msgs/msg/detail/path__functions.h"
#include "geometry_msgs/msg/detail/point__functions.h"
#include "nav_msgs/msg/detail/map_meta_data__functions.h"
#include "nav_msgs/msg/detail/occupancy_grid__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Point__EXPECTED_HASH = {1, {
    0x69, 0x63, 0x08, 0x48, 0x42, 0xa9, 0xb0, 0x44,
    0x94, 0xd6, 0xb2, 0x94, 0x1d, 0x11, 0x44, 0x47,
    0x08, 0xd8, 0x92, 0xda, 0x2f, 0x4b, 0x09, 0x84,
    0x3b, 0x9c, 0x43, 0xf4, 0x2a, 0x7f, 0x68, 0x81,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Pose__EXPECTED_HASH = {1, {
    0xd5, 0x01, 0x95, 0x4e, 0x94, 0x76, 0xce, 0xa2,
    0x99, 0x69, 0x84, 0xe8, 0x12, 0x05, 0x4b, 0x68,
    0x02, 0x6a, 0xe0, 0xbf, 0xae, 0x78, 0x9d, 0x9a,
    0x10, 0xb2, 0x3d, 0xaf, 0x35, 0xcc, 0x90, 0xfa,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__PoseStamped__EXPECTED_HASH = {1, {
    0x10, 0xf3, 0x78, 0x6d, 0x7d, 0x40, 0xfd, 0x2b,
    0x54, 0x36, 0x78, 0x35, 0x61, 0x4b, 0xff, 0x85,
    0xd4, 0xad, 0x3b, 0x5d, 0xab, 0x62, 0xbf, 0x8b,
    0xca, 0x0c, 0xc2, 0x32, 0xd7, 0x3b, 0x4c, 0xd8,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Quaternion__EXPECTED_HASH = {1, {
    0x8a, 0x76, 0x5f, 0x66, 0x77, 0x8c, 0x8f, 0xf7,
    0xc8, 0xab, 0x94, 0xaf, 0xcc, 0x59, 0x0a, 0x2e,
    0xd5, 0x32, 0x5a, 0x1d, 0x9a, 0x07, 0x6f, 0xff,
    0xf3, 0x8f, 0xbc, 0xe3, 0x6f, 0x45, 0x86, 0x84,
  }};
static const rosidl_type_hash_t nav2_msgs__msg__Costmap__EXPECTED_HASH = {1, {
    0xd5, 0x1b, 0xf7, 0xae, 0xca, 0xfd, 0xbb, 0x3f,
    0x8f, 0x98, 0x21, 0x5d, 0xe6, 0x48, 0xab, 0xe6,
    0xd5, 0x3f, 0x8d, 0xb6, 0x91, 0x56, 0xd6, 0xe1,
    0x43, 0x12, 0x5d, 0x2a, 0xd2, 0xbf, 0x00, 0x27,
  }};
static const rosidl_type_hash_t nav2_msgs__msg__CostmapMetaData__EXPECTED_HASH = {1, {
    0x1a, 0x41, 0xec, 0x84, 0x28, 0xd5, 0x0c, 0x3b,
    0x4c, 0xd3, 0xf9, 0x05, 0x5e, 0x1a, 0xdb, 0x0e,
    0xae, 0xc7, 0x2f, 0xb3, 0x9a, 0xe1, 0x16, 0x86,
    0xb5, 0x92, 0x18, 0xf6, 0xe0, 0x88, 0x4c, 0xbd,
  }};
static const rosidl_type_hash_t nav_msgs__msg__MapMetaData__EXPECTED_HASH = {1, {
    0x27, 0x72, 0xd4, 0xb2, 0x00, 0x0e, 0xf2, 0xb3,
    0x5d, 0xba, 0xeb, 0x80, 0xfd, 0x39, 0x46, 0xc1,
    0x36, 0x9f, 0x81, 0x7f, 0xb4, 0xf7, 0x56, 0x77,
    0xd9, 0x16, 0xd2, 0x7c, 0x17, 0xd7, 0x63, 0xc8,
  }};
static const rosidl_type_hash_t nav_msgs__msg__OccupancyGrid__EXPECTED_HASH = {1, {
    0x8d, 0x34, 0x81, 0x50, 0xc1, 0x29, 0x13, 0xa3,
    0x1e, 0xe0, 0xec, 0x17, 0x0f, 0xbf, 0x25, 0x08,
    0x9e, 0x47, 0x45, 0xd1, 0x70, 0x35, 0x79, 0x2a,
    0x1b, 0xa9, 0x4d, 0x6f, 0x0b, 0xc0, 0xcf, 0xc7,
  }};
static const rosidl_type_hash_t nav_msgs__msg__Path__EXPECTED_HASH = {1, {
    0x19, 0x57, 0xa5, 0xbb, 0x3c, 0xee, 0x5d, 0xa6,
    0x5c, 0x4e, 0x52, 0xe5, 0x2b, 0x65, 0xa9, 0x3d,
    0xf2, 0x27, 0xef, 0xce, 0x4c, 0x20, 0xf8, 0x45,
    0x8b, 0x36, 0xe7, 0x30, 0x66, 0xca, 0x33, 0x4b,
  }};
static const rosidl_type_hash_t std_msgs__msg__Header__EXPECTED_HASH = {1, {
    0xf4, 0x9f, 0xb3, 0xae, 0x2c, 0xf0, 0x70, 0xf7,
    0x93, 0x64, 0x5f, 0xf7, 0x49, 0x68, 0x3a, 0xc6,
    0xb0, 0x62, 0x03, 0xe4, 0x1c, 0x89, 0x1e, 0x17,
    0x70, 0x1b, 0x1c, 0xb5, 0x97, 0xce, 0x6a, 0x01,
  }};
#endif

static char saye_msgs__msg__Map__TYPE_NAME[] = "saye_msgs/msg/Map";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char geometry_msgs__msg__Point__TYPE_NAME[] = "geometry_msgs/msg/Point";
static char geometry_msgs__msg__Pose__TYPE_NAME[] = "geometry_msgs/msg/Pose";
static char geometry_msgs__msg__PoseStamped__TYPE_NAME[] = "geometry_msgs/msg/PoseStamped";
static char geometry_msgs__msg__Quaternion__TYPE_NAME[] = "geometry_msgs/msg/Quaternion";
static char nav2_msgs__msg__Costmap__TYPE_NAME[] = "nav2_msgs/msg/Costmap";
static char nav2_msgs__msg__CostmapMetaData__TYPE_NAME[] = "nav2_msgs/msg/CostmapMetaData";
static char nav_msgs__msg__MapMetaData__TYPE_NAME[] = "nav_msgs/msg/MapMetaData";
static char nav_msgs__msg__OccupancyGrid__TYPE_NAME[] = "nav_msgs/msg/OccupancyGrid";
static char nav_msgs__msg__Path__TYPE_NAME[] = "nav_msgs/msg/Path";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char saye_msgs__msg__Map__FIELD_NAME__costmap_meta_data[] = "costmap_meta_data";
static char saye_msgs__msg__Map__FIELD_NAME__costmap[] = "costmap";
static char saye_msgs__msg__Map__FIELD_NAME__occupancy_grid[] = "occupancy_grid";
static char saye_msgs__msg__Map__FIELD_NAME__map_meta_data[] = "map_meta_data";
static char saye_msgs__msg__Map__FIELD_NAME__path[] = "path";
static char saye_msgs__msg__Map__FIELD_NAME__header[] = "header";

static rosidl_runtime_c__type_description__Field saye_msgs__msg__Map__FIELDS[] = {
  {
    {saye_msgs__msg__Map__FIELD_NAME__costmap_meta_data, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {nav2_msgs__msg__CostmapMetaData__TYPE_NAME, 29, 29},
    },
    {NULL, 0, 0},
  },
  {
    {saye_msgs__msg__Map__FIELD_NAME__costmap, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {nav2_msgs__msg__Costmap__TYPE_NAME, 21, 21},
    },
    {NULL, 0, 0},
  },
  {
    {saye_msgs__msg__Map__FIELD_NAME__occupancy_grid, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {nav_msgs__msg__OccupancyGrid__TYPE_NAME, 26, 26},
    },
    {NULL, 0, 0},
  },
  {
    {saye_msgs__msg__Map__FIELD_NAME__map_meta_data, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {nav_msgs__msg__MapMetaData__TYPE_NAME, 24, 24},
    },
    {NULL, 0, 0},
  },
  {
    {saye_msgs__msg__Map__FIELD_NAME__path, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {nav_msgs__msg__Path__TYPE_NAME, 17, 17},
    },
    {NULL, 0, 0},
  },
  {
    {saye_msgs__msg__Map__FIELD_NAME__header, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription saye_msgs__msg__Map__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Pose__TYPE_NAME, 22, 22},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__PoseStamped__TYPE_NAME, 29, 29},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Quaternion__TYPE_NAME, 28, 28},
    {NULL, 0, 0},
  },
  {
    {nav2_msgs__msg__Costmap__TYPE_NAME, 21, 21},
    {NULL, 0, 0},
  },
  {
    {nav2_msgs__msg__CostmapMetaData__TYPE_NAME, 29, 29},
    {NULL, 0, 0},
  },
  {
    {nav_msgs__msg__MapMetaData__TYPE_NAME, 24, 24},
    {NULL, 0, 0},
  },
  {
    {nav_msgs__msg__OccupancyGrid__TYPE_NAME, 26, 26},
    {NULL, 0, 0},
  },
  {
    {nav_msgs__msg__Path__TYPE_NAME, 17, 17},
    {NULL, 0, 0},
  },
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
saye_msgs__msg__Map__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {saye_msgs__msg__Map__TYPE_NAME, 17, 17},
      {saye_msgs__msg__Map__FIELDS, 6, 6},
    },
    {saye_msgs__msg__Map__REFERENCED_TYPE_DESCRIPTIONS, 11, 11},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Pose__EXPECTED_HASH, geometry_msgs__msg__Pose__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = geometry_msgs__msg__Pose__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__PoseStamped__EXPECTED_HASH, geometry_msgs__msg__PoseStamped__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = geometry_msgs__msg__PoseStamped__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Quaternion__EXPECTED_HASH, geometry_msgs__msg__Quaternion__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = geometry_msgs__msg__Quaternion__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&nav2_msgs__msg__Costmap__EXPECTED_HASH, nav2_msgs__msg__Costmap__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = nav2_msgs__msg__Costmap__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&nav2_msgs__msg__CostmapMetaData__EXPECTED_HASH, nav2_msgs__msg__CostmapMetaData__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[6].fields = nav2_msgs__msg__CostmapMetaData__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&nav_msgs__msg__MapMetaData__EXPECTED_HASH, nav_msgs__msg__MapMetaData__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[7].fields = nav_msgs__msg__MapMetaData__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&nav_msgs__msg__OccupancyGrid__EXPECTED_HASH, nav_msgs__msg__OccupancyGrid__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[8].fields = nav_msgs__msg__OccupancyGrid__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&nav_msgs__msg__Path__EXPECTED_HASH, nav_msgs__msg__Path__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[9].fields = nav_msgs__msg__Path__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[10].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "nav2_msgs/CostmapMetaData costmap_meta_data\n"
  "nav2_msgs/Costmap costmap\n"
  "nav_msgs/OccupancyGrid occupancy_grid\n"
  "nav_msgs/MapMetaData map_meta_data\n"
  "nav_msgs/Path path\n"
  "std_msgs/Header header";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
saye_msgs__msg__Map__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {saye_msgs__msg__Map__TYPE_NAME, 17, 17},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 184, 184},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
saye_msgs__msg__Map__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[12];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 12, 12};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *saye_msgs__msg__Map__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    sources[3] = *geometry_msgs__msg__Pose__get_individual_type_description_source(NULL);
    sources[4] = *geometry_msgs__msg__PoseStamped__get_individual_type_description_source(NULL);
    sources[5] = *geometry_msgs__msg__Quaternion__get_individual_type_description_source(NULL);
    sources[6] = *nav2_msgs__msg__Costmap__get_individual_type_description_source(NULL);
    sources[7] = *nav2_msgs__msg__CostmapMetaData__get_individual_type_description_source(NULL);
    sources[8] = *nav_msgs__msg__MapMetaData__get_individual_type_description_source(NULL);
    sources[9] = *nav_msgs__msg__OccupancyGrid__get_individual_type_description_source(NULL);
    sources[10] = *nav_msgs__msg__Path__get_individual_type_description_source(NULL);
    sources[11] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
