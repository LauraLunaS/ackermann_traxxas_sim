#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "saye_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__saye_msgs__msg__Map() -> *const std::ffi::c_void;
}

#[link(name = "saye_msgs__rosidl_generator_c")]
extern "C" {
    fn saye_msgs__msg__Map__init(msg: *mut Map) -> bool;
    fn saye_msgs__msg__Map__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Map>, size: usize) -> bool;
    fn saye_msgs__msg__Map__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Map>);
    fn saye_msgs__msg__Map__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Map>, out_seq: *mut rosidl_runtime_rs::Sequence<Map>) -> bool;
}

// Corresponds to saye_msgs__msg__Map
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Map {

    // This member is not documented.
    #[allow(missing_docs)]
    pub costmap_meta_data: nav2_msgs::msg::rmw::CostmapMetaData,


    // This member is not documented.
    #[allow(missing_docs)]
    pub costmap: nav2_msgs::msg::rmw::Costmap,


    // This member is not documented.
    #[allow(missing_docs)]
    pub occupancy_grid: nav_msgs::msg::rmw::OccupancyGrid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub map_meta_data: nav_msgs::msg::rmw::MapMetaData,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path: nav_msgs::msg::rmw::Path,


    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

}



impl Default for Map {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !saye_msgs__msg__Map__init(&mut msg as *mut _) {
        panic!("Call to saye_msgs__msg__Map__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Map {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { saye_msgs__msg__Map__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { saye_msgs__msg__Map__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { saye_msgs__msg__Map__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Map {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Map where Self: Sized {
  const TYPE_NAME: &'static str = "saye_msgs/msg/Map";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__saye_msgs__msg__Map() }
  }
}


