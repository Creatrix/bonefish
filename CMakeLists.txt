cmake_minimum_required(VERSION 2.8)
project(bonefish)

option(shared "build bonefish as a shared library" OFF)
option(stdlib "When building with clang, you can choose libc++ (default) or libstdc++" OFF)

set(BOOST_COMPONENTS program_options system thread regex random)
if (NOT CMAKE_BUILD_TYPE)
	message("Build Type Not Set. Defaulting to Release...")
	set(CMAKE_BUILD_TYPE "Release")
endif()
execute_process(COMMAND conan install ${CMAKE_CURRENT_SOURCE_DIR} --build=missing -s build_type=${CMAKE_BUILD_TYPE})
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_BINARY_DIR})

find_file(CONAN_BUILD_INFO conanbuildinfo.cmake PATHS ${CMAKE_BINARY_DIR})

if (CONAN_BUILD_INFO)
    message("Configuring for Conan Build!")
    set(IS_CONAN_BUILD YES)
    set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_BINARY_DIR})
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
endif()

if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    if (NOT stdlib)
        set(stdlib "libc++")
    endif()
    if (CMAKE_GENERATOR STREQUAL "Ninja")
        set(CMAKE_CXX_FLAGS "-fcolor-diagnostics ${CMAKE_CXX_FLAGS}")
    endif()
    if (stdlib STREQUAL "libstdc++")
        # libstdc++ defines template<typename> friend class hash, which causes warnings
        set(CMAKE_CXX_FLAGS "-Wno-mismatched-tags ${CMAKE_CXX_FLAGS}")
    endif()
    set(CMAKE_CXX_FLAGS "-stdlib=${stdlib} -Wno-unused-local-typedefs -Wno-unknown-warning-option ${CMAKE_CXX_FLAGS}")
else()
    if(stdlib)
        message(STATUS "stdlib option (set to ${stdlib}) is ignored for ${CMAKE_CXX_COMPILER_ID} compiler")
    endif()
endif()

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    if(CMAKE_CXX_COMPILER_VERSION VERSION_LESS "4.9.0") # i.e. if < 4.9.0
        list(APPEND BOOST_COMPONENTS regex)
    add_definitions(-DUSE_BOOST_REGEX)
    else() # >= 4.9.0
        if (CMAKE_GENERATOR STREQUAL "Ninja")
            set(CMAKE_CXX_FLAGS "-fdiagnostics-color=always ${CMAKE_CXX_FLAGS}")
        else()
            set(CMAKE_CXX_FLAGS "-fdiagnostics-color=auto ${CMAKE_CXX_FLAGS}")
        endif()
    endif()
endif()

if(NOT MSVC)
    set(CMAKE_CXX_FLAGS "-Wall -Werror -Wno-unused-variable -std=c++11 ${CMAKE_CXX_FLAGS}")
else()
    add_definitions(-D_WEBSOCKETPP_CPP11_CHRONO_)
endif()

set(CMAKE_CXX_FLAGS_DEBUG "-O0 ${CMAKE_CXX_FLAGS_DEBUG}")
set(CMAKE_C_FLAGS_DEBUG "-O0 ${CMAKE_C_FLAGS_DEBUG}")

set(CMAKE_MODULE_PATH
    ${CMAKE_MODULE_PATH}
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules/")

if(shared)
    set(Boost_USE_STATIC_LIBS OFF)
    set(RT_USE_STATIC_LIBS OFF)
else()
    set(Boost_USE_STATIC_LIBS ON)
    set(RT_USE_STATIC_LIBS ON)
endif()

if(WIN32)
    add_definitions(-D_WIN32_WINNT=0x0500)
    add_definitions(-DWIN32_LEAN_AND_MEAN)
endif()


if (IS_CONAN_BUILD)
    find_package(msgpack)
    find_package(websocketpp)
    find_package(json-msgpack)
    find_package(rapidjson)
    find_package(cppcodec)
    find_package(boost_program_options)
    find_package(boost_format)
    find_package(bzip2)
else()
    find_package(Boost REQUIRED COMPONENTS ${BOOST_COMPONENTS})
endif()
if (UNIX)
    find_package(RT)
endif()

find_package(Threads)

include_directories(
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/third-party/cppcodec
    ${CMAKE_SOURCE_DIR}/third-party/json-msgpack/include
    ${CMAKE_SOURCE_DIR}/third-party/msgpack-c/include
    #${CMAKE_SOURCE_DIR}/third-party/rapidjson/include
    #${CMAKE_SOURCE_DIR}/third-party/websocketpp
    ${Boost_INCLUDE_DIRS}
)

if(WIN32)
include_directories(${CMAKE_PREFIX_PATH})
endif()

link_directories(${CMAKE_INSTALL_PREFIX}/lib)

add_subdirectory(examples)
add_subdirectory(src)
add_subdirectory(daemon)
add_subdirectory(test)
