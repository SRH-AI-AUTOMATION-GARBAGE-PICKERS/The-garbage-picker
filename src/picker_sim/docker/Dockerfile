FROM osrf/ros:humble-desktop
RUN apt-get update && apt-get install -y \
    ros-humble-ros-gz ros-humble-navigation2 ros-humble-xacro mesa-utils \
    && rm -rf /var/lib/apt/lists/*
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
