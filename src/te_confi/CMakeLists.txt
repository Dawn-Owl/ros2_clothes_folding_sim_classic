cmake_minimum_required(VERSION 3.8)
project(te_confi)

find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)

install(
  DIRECTORY urdf meshes launch worlds config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

