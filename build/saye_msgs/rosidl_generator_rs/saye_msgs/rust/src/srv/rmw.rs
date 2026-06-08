#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "saye_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__saye_msgs__srv__ShareMap_Request() -> *const std::ffi::c_void;
}

#[link(name = "saye_msgs__rosidl_generator_c")]
extern "C" {
    fn saye_msgs__srv__ShareMap_Request__init(msg: *mut ShareMap_Request) -> bool;
    fn saye_msgs__srv__ShareMap_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ShareMap_Request>, size: usize) -> bool;
    fn saye_msgs__srv__ShareMap_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ShareMap_Request>);
    fn saye_msgs__srv__ShareMap_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ShareMap_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ShareMap_Request>) -> bool;
}

// Corresponds to saye_msgs__srv__ShareMap_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ShareMap_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub topic_name: rosidl_runtime_rs::String,

}



impl Default for ShareMap_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !saye_msgs__srv__ShareMap_Request__init(&mut msg as *mut _) {
        panic!("Call to saye_msgs__srv__ShareMap_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ShareMap_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { saye_msgs__srv__ShareMap_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { saye_msgs__srv__ShareMap_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { saye_msgs__srv__ShareMap_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ShareMap_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ShareMap_Request where Self: Sized {
  const TYPE_NAME: &'static str = "saye_msgs/srv/ShareMap_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__saye_msgs__srv__ShareMap_Request() }
  }
}


#[link(name = "saye_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__saye_msgs__srv__ShareMap_Response() -> *const std::ffi::c_void;
}

#[link(name = "saye_msgs__rosidl_generator_c")]
extern "C" {
    fn saye_msgs__srv__ShareMap_Response__init(msg: *mut ShareMap_Response) -> bool;
    fn saye_msgs__srv__ShareMap_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ShareMap_Response>, size: usize) -> bool;
    fn saye_msgs__srv__ShareMap_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ShareMap_Response>);
    fn saye_msgs__srv__ShareMap_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ShareMap_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ShareMap_Response>) -> bool;
}

// Corresponds to saye_msgs__srv__ShareMap_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ShareMap_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_completed: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub custom_occupany_grid: nav_msgs::msg::rmw::OccupancyGrid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for ShareMap_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !saye_msgs__srv__ShareMap_Response__init(&mut msg as *mut _) {
        panic!("Call to saye_msgs__srv__ShareMap_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ShareMap_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { saye_msgs__srv__ShareMap_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { saye_msgs__srv__ShareMap_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { saye_msgs__srv__ShareMap_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ShareMap_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ShareMap_Response where Self: Sized {
  const TYPE_NAME: &'static str = "saye_msgs/srv/ShareMap_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__saye_msgs__srv__ShareMap_Response() }
  }
}






#[link(name = "saye_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__saye_msgs__srv__ShareMap() -> *const std::ffi::c_void;
}

// Corresponds to saye_msgs__srv__ShareMap
#[allow(missing_docs, non_camel_case_types)]
pub struct ShareMap;

impl rosidl_runtime_rs::Service for ShareMap {
    type Request = ShareMap_Request;
    type Response = ShareMap_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__saye_msgs__srv__ShareMap() }
    }
}


