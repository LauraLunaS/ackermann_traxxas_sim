#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to saye_msgs__msg__Map

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Map {

    // This member is not documented.
    #[allow(missing_docs)]
    pub costmap_meta_data: nav2_msgs::msg::CostmapMetaData,


    // This member is not documented.
    #[allow(missing_docs)]
    pub costmap: nav2_msgs::msg::Costmap,


    // This member is not documented.
    #[allow(missing_docs)]
    pub occupancy_grid: nav_msgs::msg::OccupancyGrid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub map_meta_data: nav_msgs::msg::MapMetaData,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path: nav_msgs::msg::Path,


    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

}



impl Default for Map {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Map::default())
  }
}

impl rosidl_runtime_rs::Message for Map {
  type RmwMsg = super::msg::rmw::Map;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        costmap_meta_data: nav2_msgs::msg::CostmapMetaData::into_rmw_message(std::borrow::Cow::Owned(msg.costmap_meta_data)).into_owned(),
        costmap: nav2_msgs::msg::Costmap::into_rmw_message(std::borrow::Cow::Owned(msg.costmap)).into_owned(),
        occupancy_grid: nav_msgs::msg::OccupancyGrid::into_rmw_message(std::borrow::Cow::Owned(msg.occupancy_grid)).into_owned(),
        map_meta_data: nav_msgs::msg::MapMetaData::into_rmw_message(std::borrow::Cow::Owned(msg.map_meta_data)).into_owned(),
        path: nav_msgs::msg::Path::into_rmw_message(std::borrow::Cow::Owned(msg.path)).into_owned(),
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        costmap_meta_data: nav2_msgs::msg::CostmapMetaData::into_rmw_message(std::borrow::Cow::Borrowed(&msg.costmap_meta_data)).into_owned(),
        costmap: nav2_msgs::msg::Costmap::into_rmw_message(std::borrow::Cow::Borrowed(&msg.costmap)).into_owned(),
        occupancy_grid: nav_msgs::msg::OccupancyGrid::into_rmw_message(std::borrow::Cow::Borrowed(&msg.occupancy_grid)).into_owned(),
        map_meta_data: nav_msgs::msg::MapMetaData::into_rmw_message(std::borrow::Cow::Borrowed(&msg.map_meta_data)).into_owned(),
        path: nav_msgs::msg::Path::into_rmw_message(std::borrow::Cow::Borrowed(&msg.path)).into_owned(),
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      costmap_meta_data: nav2_msgs::msg::CostmapMetaData::from_rmw_message(msg.costmap_meta_data),
      costmap: nav2_msgs::msg::Costmap::from_rmw_message(msg.costmap),
      occupancy_grid: nav_msgs::msg::OccupancyGrid::from_rmw_message(msg.occupancy_grid),
      map_meta_data: nav_msgs::msg::MapMetaData::from_rmw_message(msg.map_meta_data),
      path: nav_msgs::msg::Path::from_rmw_message(msg.path),
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
    }
  }
}


