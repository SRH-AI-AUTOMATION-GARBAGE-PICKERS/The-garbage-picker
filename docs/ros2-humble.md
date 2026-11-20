# ROS 2 Humble setup and verification

This guide prepares a compatible Team Picker laptop with ROS 2 Humble. The
supported target for this guide is **Ubuntu 22.04 (Jammy) on amd64**. ROS 2
Humble is also available for other platforms, but the commands below are for
the Ubuntu deb packages.

## Install ROS 2 Humble

Run the following commands in a terminal:

```bash
sudo apt update && sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install -y curl

sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && printf '%s' "$UBUNTU_CODENAME") main" |
  sudo tee /etc/apt/sources.list.d/ros2.list >/dev/null

sudo apt update
sudo apt install -y ros-humble-desktop
```

The package installs ROS 2 under `/opt/ros/humble`. Check that the laptop is
the expected Ubuntu release before installing:

```bash
. /etc/os-release && printf '%s %s\n' "$NAME" "$VERSION_ID"
```

## Configure the shell

Source the ROS 2 environment in every shell that uses ROS 2:

```bash
source /opt/ros/humble/setup.bash
```

To configure new Bash terminals automatically, add it once to `~/.bashrc`:

```bash
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

Do not add the line repeatedly. If a workspace is created later, source its
`install/setup.bash` after the Humble setup script.

## Verify the command-line tools

In a new terminal, run:

```bash
source /opt/ros/humble/setup.bash
ros2 --help
ros2 topic list
```

`ros2 --help` should print the available ROS 2 commands. `ros2 topic list`
should return without a setup or library error; an empty list is normal before
any nodes are running.

## Verify publisher/subscriber communication

Use two terminals, sourcing `/opt/ros/humble/setup.bash` in both.

In terminal 1, start the publisher:

```bash
ros2 run demo_nodes_cpp talker
```

In terminal 2, start the subscriber:

```bash
ros2 run demo_nodes_cpp listener
```

The publisher should print messages such as `Publishing: 'Hello World: 1'`
and the subscriber should print corresponding `I heard: [Hello World: 1]`
messages. Stop both processes with `Ctrl-C`. While they are running,
`ros2 topic list` should include `/chatter` and `/parameter_events`.

## Evidence to record

For each laptop, record the Ubuntu version, the output of `ros2 --help` and
`ros2 topic list`, and matching talker/listener output. Add the result to
`docs/laptops.md` and link terminal logs or screenshots from the issue.
