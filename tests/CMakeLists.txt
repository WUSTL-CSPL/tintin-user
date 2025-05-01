cmake_minimum_required(VERSION 3.10)

project(toy_examples)
list(APPEND CMAKE_LIBRARY_PATH "/usr/local/lib")

include_directories(../include)

file(GLOB_RECURSE SOURCE_FILES "*.c")

foreach(FILE ${SOURCE_FILES})
    get_filename_component(FILE_NAME ${FILE} NAME_WE)
  add_executable(${FILE_NAME} ${FILE})
  # pfm is for the pond related executables
  target_link_libraries(${FILE_NAME} pfm)
endforeach()

# target_link_libraries(pond_model_events pfm)
