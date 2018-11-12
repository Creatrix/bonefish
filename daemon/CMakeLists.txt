set(SOURCES bonefish.cpp daemon.cpp daemon_options.cpp)

add_executable(bonefish_bin ${SOURCES})

set_target_properties(bonefish_bin PROPERTIES OUTPUT_NAME bonefish)

add_dependencies(bonefish_bin bonefish)

if (IS_CONAN_BUILD)
    set(BONEFISH_BIN_LIBS Threads::Threads boost_program_options::boost_program_options boost_system::boost_system boost_thread::boost_thread boost_regex::boost_regex boost_random::boost_random msgpack::msgpack websocketpp::websocketpp json-msgpack::json-msgpack rapidjson::rapidjson cppcodec::cppcodec)
else()
    set(BONEFISH_BIN_LIBS ${Boost_LIBRARIES})
endif()
target_link_libraries(bonefish_bin
    bonefish
    ${BONEFISH_BIN_LIBS}
    ${CMAKE_DL_LIBS}
    ${CMAKE_THREAD_LIBS_INIT})

if (RT_FOUND)
    target_link_libraries(bonefish_bin ${RT_LIBRARIES})
endif()

install(TARGETS bonefish_bin DESTINATION bin)
