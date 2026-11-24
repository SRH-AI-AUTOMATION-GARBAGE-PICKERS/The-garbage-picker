"""Stop the Picker base: send one zero Twist on /controller/cmd_vel and exit.

  ros2 run picker_sim stop

A new ROS node needs a moment to discover the robot. A message published
before that is dropped without an error, so this waits until the base's
subscriber is matched, then publishes once. cmd_vel is RELIABLE, so one
message is delivered once matched. Exits 1 if nothing is listening after
TIMEOUT_S.

Another publisher still sending motion (teleop with a key held) overrides
this stop on its next message. Release the keys or close it first.

This is a protective stop in software, not an e-stop (SR-02).
"""
import sys
import time

import rclpy
from geometry_msgs.msg import Twist

TOPIC = '/controller/cmd_vel'
TIMEOUT_S = 2.0


def send_stop(node, pub, timeout=TIMEOUT_S):
    """Wait for a subscriber, publish zero Twist. Returns True if sent."""
    deadline = time.monotonic() + timeout
    while pub.get_subscription_count() == 0:
        if time.monotonic() > deadline:
            return False
        rclpy.spin_once(node, timeout_sec=0.01)
    pub.publish(Twist())
    return True


def main():
    rclpy.init()
    node = rclpy.create_node('picker_stop')
    pub = node.create_publisher(Twist, TOPIC, 10)
    ok = send_stop(node, pub)
    if ok:
        node.get_logger().info(f'Stop sent on {TOPIC}')
        # Let DDS flush the message before the node is destroyed.
        rclpy.spin_once(node, timeout_sec=0.2)
    else:
        node.get_logger().error(f'No subscriber on {TOPIC} after {TIMEOUT_S} s, stop NOT delivered')
    node.destroy_node()
    rclpy.try_shutdown()
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
