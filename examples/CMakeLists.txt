set(SOURCES integration.cpp)

add_executable(integration ${SOURCES})

add_dependencies(integration bonefish)

target_link_libraries(integration
    bonefish
    boost_format::boost_format
    ${Boost_LIBRARIES}
    ${CMAKE_DL_LIBS}
    ${CMAKE_THREAD_LIBS_INIT})

if (RT_FOUND)
    target_link_libraries(integration ${RT_LIBRARIES})
endif()
