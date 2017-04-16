INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MONITOR monitor)

FIND_PATH(
    MONITOR_INCLUDE_DIRS
    NAMES monitor/api.h
    HINTS $ENV{MONITOR_DIR}/include
        ${PC_MONITOR_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MONITOR_LIBRARIES
    NAMES gnuradio-monitor
    HINTS $ENV{MONITOR_DIR}/lib
        ${PC_MONITOR_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MONITOR DEFAULT_MSG MONITOR_LIBRARIES MONITOR_INCLUDE_DIRS)
MARK_AS_ADVANCED(MONITOR_LIBRARIES MONITOR_INCLUDE_DIRS)

