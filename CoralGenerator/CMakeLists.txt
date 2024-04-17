cmake_minimum_required(VERSION 3.10)
project(generateCoralReef)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set( CMAKE_BUILD_TYPE "Release")
set( CMAKE_CXX_FLAGS "-O2" )

include_directories(/opt/homebrew/include)

add_executable(${PROJECT_NAME} PerlinNoise.cpp generateCoralReef.cpp)

link_directories(/opt/homebrew/Cellar)

add_compile_options(-fdiagnostics-color=always -g)
