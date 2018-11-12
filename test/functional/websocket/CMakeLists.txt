set(SOURCES client.cpp)

add_executable(client ${SOURCES})

if (IS_CONAN_BUILD)
	set(BONEFISH_LINK_LIBS Threads::Threads boost_program_options::boost_program_options boost_system::boost_system boost_thread::boost_thread boost_regex::boost_regex boost_random::boost_random msgpack::msgpack websocketpp::websocketpp json-msgpack::json-msgpack rapidjson::rapidjson cppcodec::cppcodec)
else()
	set(BONEFISH_LINK_LIBS ${Boost_LIBRARIES} ${CMAKE_DL_LIBS} ${CMAKE_THREAD_LIBS_INIT})
endif()

target_link_libraries(client ${BONEFISH_LINK_LIBS})

if (RT_FOUND)
	target_link_libraries(client ${RT_LIBRARIES})
endif()
