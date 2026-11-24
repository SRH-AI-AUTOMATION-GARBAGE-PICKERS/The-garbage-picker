# picker_sim

Gazebo simulation of the Picker robot (Hiwonder ClawPi Ultimate: Raspberry Pi 5, mecanum base, COIN-D6 LiDAR) for the AI and Autonomous Systems Lab, SRH Leipzig.

Stack: ROS 2 Humble + Gazebo Fortress, the same ROS distro the Hiwonder Docker image is assumed to use. Topic and frame names match the real robot's software (github.com/Hiwonder/ClawPi), so a node tested here runs on the robot without remapping.

Version 0.3.0. The base can drive forward/back, strafe sideways and turn in place. The arm isn't modelled; the claw is a fixed link, same as Hiwonder's URDF.

## Contents

| Path | What it is |
|---|---|
| `urdf/picker.urdf.xacro` | Robot: Hiwonder meshes and frames, box collision, 1.13 kg, LiDAR, holonomic drive, odometry |
| `worlds/picker_lab.sdf` | 6 x 6 m fenced area, a 0.4 m crate at (1.5, 1.0), a person proxy cylinder at (2.0, -1.0) |
| `launch/sim.launch.py` | Gazebo, robot_state_publisher, spawn, ROS-Gazebo bridges, RViz |
| `picker_sim/teleop.py` | Keyboard teleop for the mecanum base (IJKL + UO) |
| `rviz/picker.rviz` | Top-down view in `odom`: robot model, TF, scan, odometry |
| `docker/Dockerfile` | Humble + Gazebo image for machines that aren't on Ubuntu 22.04 |

## 1. Setup

You need ROS 2 Humble with `ros_gz`, which means Ubuntu 22.04. There are three ways to get it.

### Option A: Ubuntu 22.04 (native or dual boot)

```bash
sudo apt install ros-humble-desktop ros-dev-tools ros-humble-ros-gz \
                 ros-humble-navigation2 ros-humble-xacro
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc   # replace with the team's agreed ID (SR-31)
```

The full Humble apt repository setup is in the official install guide: docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html

### Option B: Windows 11 with WSL2

Install the Ubuntu-22.04 distro (`wsl --install -d Ubuntu-22.04`), then do Option A inside it. Two WSL-specific things:

1. Gazebo Fortress crashes on GPU rendering under WSLg (`Ogre::UnimplementedException` in ogre2). Force CPU rendering:
   ```bash
   echo "export LIBGL_ALWAYS_SOFTWARE=1" >> ~/.bashrc
   ```
   Don't set `GALLIUM_DRIVER=d3d12`.
2. To reach the real robot over DDS later, put this in `%UserProfile%\.wslconfig` and run `wsl --shutdown` once:
   ```ini
   [wsl2]
   networkingMode=mirrored
   ```

Keep the workspace in the Linux home (`~/ros2_ws`), never under `/mnt/c`; builds there are slow and file watching breaks.

### Option C: any other Linux (e.g. Ubuntu 24.04) with Docker

Humble has no packages for 24.04, so it runs in a container. Clone the team repo first (section 2, the `git clone` line), then build the image once from this package's Dockerfile:

```bash
docker build -t picker-humble ~/ros2_ws/src/The-garbage-picker/src/picker_sim/docker
```

Create the container once. It shares the host network (needed for DDS to the robot), the GPU and the X display, and mounts `~/ros2_ws`:

```bash
xhost +local:docker
docker run -it --name humble --network host --ipc host --device /dev/dri \
  -e DISPLAY=$DISPLAY -e ROS_DOMAIN_ID=42 \
  -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/ros2_ws:/root/ros2_ws \
  picker-humble bash
```

Daily use:

| Action | Command (on the host) |
|---|---|
| Start and enter | `xhost +local:docker && docker start -ai humble` |
| Second terminal | `docker exec -it humble bash` |
| Stop | `exit` in the first terminal, or `docker stop humble` |

Edit files and run git on the host; run ROS commands in the container (prompt `root@...`). `~/ros2_ws` on the host is `/root/ros2_ws` in the container. If `docker` says permission denied, your user isn't in the `docker` group yet: `sudo usermod -aG docker $USER`, then log out and back in.

## 2. Get the workspace

The team repo goes inside the workspace's `src/`; colcon searches it recursively. Don't keep a second copy of `picker_sim` elsewhere in `src/`, or colcon fails on the duplicate package name.

This package depends on `clawpi_description` from Hiwonder's repo for the meshes. The meshes are in Git LFS, so a plain clone only gives you 130-byte pointer files.

```bash
mkdir -p ~/ros2_ws/src
git clone https://github.com/SRH-AI-AUTOMATION-GARBAGE-PICKERS/The-garbage-picker.git \
    ~/ros2_ws/src/The-garbage-picker   # colcon finds src/picker_sim inside it

sudo apt install git-lfs
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/Hiwonder/ClawPi.git ~/ClawPi
cd ~/ClawPi && git lfs pull --include="src/simulations/clawpi_description/meshes/*"
cp -r src/simulations/clawpi_description ~/ros2_ws/src/
ls -l ~/ros2_ws/src/clawpi_description/meshes/base_link.STL   # ~9 MB, not ~130 bytes
```

## 3. Build

From here on, in the ROS environment (WSL shell, native shell, or inside the container):

```bash
cd ~/ros2_ws          # /root/ros2_ws in Docker
colcon build --symlink-install
source install/setup.bash
```

With `--symlink-install`, edits to Python, launch, URDF, world and RViz files take effect on the next launch without a rebuild. Rebuild after adding a new file or changing `setup.py`.

Every new terminal needs `source ~/ros2_ws/install/setup.bash` (or add it to `~/.bashrc`).

## 4. Launch

```bash
ros2 launch picker_sim sim.launch.py              # Gazebo + RViz
ros2 launch picker_sim sim.launch.py rviz:=false  # Gazebo only
```

The robot spawns about 5 s after Gazebo starts. The delay gives the world time to load on slow machines. The simulation starts running immediately (`-r`).

On the Celeron laptop (Intel UHD 600) the real-time factor sits around 71-75 %, so 1 s of sim time takes about 1.35 s of wall time. Nodes that care about time run on `use_sim_time`, so timing-based tests stay correct; they just take longer.

Gazebo controls you'll use:
- Move the person proxy for LiDAR zone tests: select it, press `T` (Translate), drag the arrows.
- Show the collision box: right-click the robot, View > Collisions.
- Pause/play: the button at the bottom left.

## 5. Drive the robot

In a second terminal:

```bash
ros2 run picker_sim teleop
```

A small window opens. Click it so it has keyboard focus, then hold keys:

| Key | Motion | Twist field |
|---|---|---|
| I / K | forward / backward | `linear.x` + / - |
| J / L | strafe left / right, heading unchanged | `linear.y` + / - |
| U / O | turn in place left / right (CCW / CW) | `angular.z` + / - |

Releasing the key stops the robot. Keys combine: I+J drives diagonally, I+U drives an arc, opposite keys cancel. A diagonal is scaled to the same speed as a straight move, not 1.41 times faster.

The teleop is a window, not a terminal program, because a terminal never receives key-release events. With auto-repeat (500 ms delay on most desktops) a terminal teleop either stutters or keeps driving for half a second after you let go.

Safety behaviour:
- Default speed is 0.15 m/s and 0.5 rad/s, 50 % of the SR-05 limits, as SR-23 requires for new motion code.
- Change it with parameters. Anything above SR-05 (0.3 m/s, 1.0 rad/s) is clamped with a warning; the limits are constants in the code, not parameters.
  ```bash
  ros2 run picker_sim teleop --ros-args -p linear_speed:=0.3 -p angular_speed:=1.0
  ```
- The window publishes at 20 Hz, zeros when nothing is held.
- Clicking another window stops the robot (that window would get the key-release, so the teleop clears all keys on focus loss).
- Closing the window, Ctrl+C or `kill` publishes a final zero Twist before exiting.

Without the teleop, send a command by hand:

```bash
ros2 topic pub -r 20 /controller/cmd_vel geometry_msgs/msg/Twist "{linear: {y: 0.15}}"
# Ctrl+C, then stop it explicitly; the base keeps the last command:
ros2 topic pub --once /controller/cmd_vel geometry_msgs/msg/Twist "{}"
```

## 6. ROS interface

| Topic | Direction | Type | Notes |
|---|---|---|---|
| `/controller/cmd_vel` | in | `geometry_msgs/Twist` | `linear.x`, `linear.y`, `angular.z`, body frame |
| `/scan_raw` | out | `sensor_msgs/LaserScan` | frame `lidar_frame`, 400 samples / 360°, 10 Hz, 0.05-12 m, noise σ 0.01 m |
| `/odom` | out | `nav_msgs/Odometry` | ground truth from Gazebo, 50 Hz |
| `/tf` | out | | `odom` → `base_footprint` from Gazebo; `base_link`, `lidar_link`, `lidar_frame`, `imu_link`, `claw_link` from robot_state_publisher |
| `/clock` | out | `rosgraph_msgs/Clock` | sim time |

Quick checks:

```bash
ros2 topic list
ros2 topic echo /scan_raw --once --field header     # frame_id: lidar_frame
ros2 topic echo /odom --once --field pose.pose
ros2 topic hz /controller/cmd_vel                   # ~20 Hz with teleop open
```

## 7. Running against the real robot

The same teleop drives the robot: Hiwonder's `odom_publisher_node.py` subscribes to `/controller/cmd_vel` and feeds `linear.x`, `linear.y` and `angular.z` into its mecanum kinematics (`controller/mecanum.py`).

1. Same Wi-Fi as the robot, same `ROS_DOMAIN_ID` on both sides.
2. If NordVPN is installed: `nordvpn set lan-discovery on`, otherwise DDS discovery is blocked.
3. Check you can see the robot: `ros2 topic list` should show `/scan_raw` and `/odom` from the robot.
4. Run `ros2 run picker_sim teleop` at the default 50 % speed, with someone at the power switch.

## 8. Known limitations

- No command watchdog yet (SR-03). Both the Gazebo VelocityControl plugin and Hiwonder's controller keep executing the last Twist they received. If the teleop dies without sending its final zero, or the network drops, the robot keeps moving. The safety node (next step) will add the 500 ms timeout.
- No speed limiter on `/controller/cmd_vel` itself (SR-05). The teleop clamps its own output, but any other publisher can send any speed.
- The robot's own odometry ignores strafing. `cal_odom_fun` in Hiwonder's `odom_publisher_node.py` integrates only `linear_x` and `angular_z`, so on the real robot `/odom` drifts whenever it moves sideways. The simulation publishes ground truth and doesn't show this.
- The base moves by setting velocity directly (VelocityControl) on a frictionless box, not by simulated wheel contact. There's no wheel slip and no acceleration limit, so stopping-distance results (SR-13) from the sim are a lower bound.
- The collision box (313.5 x 170 x 110 mm, centred on `base_link`) still needs a visual check against the mesh.
- Arm joints aren't modelled, so SR-04 and SR-20 can't be tested yet.

## 9. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Gazebo shows a plain box instead of the ClawPi | An old build is still installed. `rm -rf build/picker_sim install/picker_sim`, rebuild, re-source. |
| Robot invisible or mesh errors in the log | Meshes are LFS pointers. Check `base_link.STL` is ~9 MB; redo the `git lfs pull` from section 2. |
| Gazebo crashes with `Ogre::UnimplementedException` (WSL) | `export LIBGL_ALWAYS_SOFTWARE=1`, see Option B. |
| `cannot open display` in Docker | Run `xhost +local:docker` on the host before `docker start`. |
| `Package 'picker_sim' not found` | You didn't `source install/setup.bash` in this terminal. |
| Teleop window open but robot doesn't move | The window doesn't have focus; click it. Check `ros2 topic hz /controller/cmd_vel`. |
| Can't see the robot's topics | Different `ROS_DOMAIN_ID`, VPN blocking LAN (`nordvpn set lan-discovery on`), or WSL without mirrored networking. |
| `xacro: command not found` on launch | `sudo apt install ros-humble-xacro` (the Dockerfile already includes it). |
