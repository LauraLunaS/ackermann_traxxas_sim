# generated from rosidl_generator_py/resource/_idl.py.em
# with input from saye_msgs:msg/Map.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Map(type):
    """Metaclass of message 'Map'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('saye_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'saye_msgs.msg.Map')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__map
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__map
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__map
            cls._TYPE_SUPPORT = module.type_support_msg__msg__map
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__map

            from nav2_msgs.msg import Costmap
            if Costmap.__class__._TYPE_SUPPORT is None:
                Costmap.__class__.__import_type_support__()

            from nav2_msgs.msg import CostmapMetaData
            if CostmapMetaData.__class__._TYPE_SUPPORT is None:
                CostmapMetaData.__class__.__import_type_support__()

            from nav_msgs.msg import MapMetaData
            if MapMetaData.__class__._TYPE_SUPPORT is None:
                MapMetaData.__class__.__import_type_support__()

            from nav_msgs.msg import OccupancyGrid
            if OccupancyGrid.__class__._TYPE_SUPPORT is None:
                OccupancyGrid.__class__.__import_type_support__()

            from nav_msgs.msg import Path
            if Path.__class__._TYPE_SUPPORT is None:
                Path.__class__.__import_type_support__()

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Map(metaclass=Metaclass_Map):
    """Message class 'Map'."""

    __slots__ = [
        '_costmap_meta_data',
        '_costmap',
        '_occupancy_grid',
        '_map_meta_data',
        '_path',
        '_header',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'costmap_meta_data': 'nav2_msgs/CostmapMetaData',
        'costmap': 'nav2_msgs/Costmap',
        'occupancy_grid': 'nav_msgs/OccupancyGrid',
        'map_meta_data': 'nav_msgs/MapMetaData',
        'path': 'nav_msgs/Path',
        'header': 'std_msgs/Header',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['nav2_msgs', 'msg'], 'CostmapMetaData'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['nav2_msgs', 'msg'], 'Costmap'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['nav_msgs', 'msg'], 'OccupancyGrid'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['nav_msgs', 'msg'], 'MapMetaData'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['nav_msgs', 'msg'], 'Path'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from nav2_msgs.msg import CostmapMetaData
        self.costmap_meta_data = kwargs.get('costmap_meta_data', CostmapMetaData())
        from nav2_msgs.msg import Costmap
        self.costmap = kwargs.get('costmap', Costmap())
        from nav_msgs.msg import OccupancyGrid
        self.occupancy_grid = kwargs.get('occupancy_grid', OccupancyGrid())
        from nav_msgs.msg import MapMetaData
        self.map_meta_data = kwargs.get('map_meta_data', MapMetaData())
        from nav_msgs.msg import Path
        self.path = kwargs.get('path', Path())
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.costmap_meta_data != other.costmap_meta_data:
            return False
        if self.costmap != other.costmap:
            return False
        if self.occupancy_grid != other.occupancy_grid:
            return False
        if self.map_meta_data != other.map_meta_data:
            return False
        if self.path != other.path:
            return False
        if self.header != other.header:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def costmap_meta_data(self):
        """Message field 'costmap_meta_data'."""
        return self._costmap_meta_data

    @costmap_meta_data.setter
    def costmap_meta_data(self, value):
        if self._check_fields:
            from nav2_msgs.msg import CostmapMetaData
            assert \
                isinstance(value, CostmapMetaData), \
                "The 'costmap_meta_data' field must be a sub message of type 'CostmapMetaData'"
        self._costmap_meta_data = value

    @builtins.property
    def costmap(self):
        """Message field 'costmap'."""
        return self._costmap

    @costmap.setter
    def costmap(self, value):
        if self._check_fields:
            from nav2_msgs.msg import Costmap
            assert \
                isinstance(value, Costmap), \
                "The 'costmap' field must be a sub message of type 'Costmap'"
        self._costmap = value

    @builtins.property
    def occupancy_grid(self):
        """Message field 'occupancy_grid'."""
        return self._occupancy_grid

    @occupancy_grid.setter
    def occupancy_grid(self, value):
        if self._check_fields:
            from nav_msgs.msg import OccupancyGrid
            assert \
                isinstance(value, OccupancyGrid), \
                "The 'occupancy_grid' field must be a sub message of type 'OccupancyGrid'"
        self._occupancy_grid = value

    @builtins.property
    def map_meta_data(self):
        """Message field 'map_meta_data'."""
        return self._map_meta_data

    @map_meta_data.setter
    def map_meta_data(self, value):
        if self._check_fields:
            from nav_msgs.msg import MapMetaData
            assert \
                isinstance(value, MapMetaData), \
                "The 'map_meta_data' field must be a sub message of type 'MapMetaData'"
        self._map_meta_data = value

    @builtins.property
    def path(self):
        """Message field 'path'."""
        return self._path

    @path.setter
    def path(self, value):
        if self._check_fields:
            from nav_msgs.msg import Path
            assert \
                isinstance(value, Path), \
                "The 'path' field must be a sub message of type 'Path'"
        self._path = value

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if self._check_fields:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value
