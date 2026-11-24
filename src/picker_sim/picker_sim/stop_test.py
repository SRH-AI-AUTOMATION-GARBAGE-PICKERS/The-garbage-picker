"""Issue #16: repeated stop test for the Picker base (sim or real robot).

  ros2 run picker_sim stop_test
  ros2 run picker_sim stop_test --ros-args -p runs:=10 -p speeds:=[0.15]

Each run drives straight at the given speed for DRIVE_S, sends the stop
(same message as `ros2 run picker_sim stop`), then watches /odom for
WATCH_S. Runs alternate forward/backward so the robot stays near its start.

Per run it reports:
  stop time  wall time from sending the stop until /odom speed drops below
             STILL_SPEED and stays there
  distance   travel from the stop moment until rest
  stays      True if the robot didn't move again during the watch window
PASS needs: stopped, stays stopped, and distance <= SR-13's 0.15 m.

Close the teleop first; it publishes on the same topic at 20 Hz.
"""
import math
import signal
import time

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.signals import SignalHandlerOptions

from picker_sim.stop import TOPIC, send_stop

MAX_LINEAR = 0.3     # SR-05, m/s
MAX_STOP_DIST = 0.15  # SR-13, m
STILL_SPEED = 0.005  # m/s, below this counts as stopped
DRIVE_S = 2.0
WATCH_S = 1.5
RATE_HZ = 20.0


def analyse(samples, t_stop, start_xy):
    """samples: [(wall_t, x, y, speed)] received after t_stop.

    Returns (stop_time_s or None, distance_m, stays_stopped).
    """
    rest = None  # index of the first sample from which the robot stays still
    for i, (_, _, _, v) in enumerate(samples):
        if v >= STILL_SPEED:
            rest = None
        elif rest is None:
            rest = i
    if rest is None:
        last = samples[-1] if samples else (t_stop, *start_xy, 0.0)
        return None, math.dist(start_xy, last[1:3]), False
    t, x, y, _ = samples[rest]
    moved_again = any(v >= STILL_SPEED for _, _, _, v in samples[rest:])
    return t - t_stop, math.dist(start_xy, (x, y)), not moved_again


class StopTest:

    def __init__(self, node):
        self.node = node
        self.pub = node.create_publisher(Twist, TOPIC, 10)
        self.odom = None  # (wall_t, x, y, speed)
        self.log = None   # list to record samples into, or None
        node.create_subscription(Odometry, '/odom', self.on_odom, 50)

    def on_odom(self, msg):
        p, v = msg.pose.pose.position, msg.twist.twist.linear
        self.odom = (time.monotonic(), p.x, p.y, math.hypot(v.x, v.y))
        if self.log is not None:
            self.log.append(self.odom)

    def spin_for(self, seconds):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            rclpy.spin_once(self.node, timeout_sec=0.005)

    def run(self, speed):
        drive = Twist()
        drive.linear.x = speed
        period = 1.0 / RATE_HZ
        end = time.monotonic() + DRIVE_S
        while time.monotonic() < end:
            self.pub.publish(drive)
            self.spin_for(period)
        _, x0, y0, v0 = self.odom
        self.log = []
        t_stop = time.monotonic()
        send_stop(self.node, self.pub)
        self.spin_for(WATCH_S)
        samples, self.log = self.log, None
        return (v0, *analyse(samples, t_stop, (x0, y0)))


def main():
    # Own signal handling (same as teleop): rclpy's handler would invalidate
    # the context before the final zero Twist in `finally` is published, and
    # Ctrl+C would leave the robot driving.
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
    signal.signal(signal.SIGTERM, signal.default_int_handler)  # kill -> same path as Ctrl+C
    node = rclpy.create_node('picker_stop_test')
    runs = node.declare_parameter('runs', 5).value
    speeds = node.declare_parameter('speeds', [0.15, 0.3]).value
    test = StopTest(node)
    rows = []
    try:
        if not send_stop(node, test.pub):
            node.get_logger().error(f'Nothing subscribed to {TOPIC}. Is the sim running?')
            return
        while test.odom is None:
            rclpy.spin_once(node, timeout_sec=0.1)
        test.spin_for(1.0)  # start from rest

        n = 0
        for speed in speeds:
            speed = min(abs(speed), MAX_LINEAR)
            for _ in range(runs):
                direction = 1 if n % 2 == 0 else -1
                n += 1
                v0, t, dist, stays = test.run(direction * speed)
                ok = t is not None and stays and dist <= MAX_STOP_DIST
                rows.append((n, direction * speed, v0, t, dist, stays, ok))
                print(f'run {n}: cmd {direction * speed:+.2f} m/s -> '
                      f'{"stopped in %.0f ms" % (t * 1000) if t is not None else "DID NOT STOP"}, '
                      f'{dist * 100:.1f} cm, {"PASS" if ok else "FAIL"}', flush=True)
                test.spin_for(0.5)
    except KeyboardInterrupt:
        print('\nInterrupted, stopping the robot')
    finally:
        test.pub.publish(Twist())  # never leave the robot driving
        rclpy.spin_once(node, timeout_sec=0.2)

    print('\n| Run | Command (m/s) | Speed at stop (m/s) | Stop time (ms) '
          '| Distance (cm) | Stays stopped | Result |')
    print('|---|---|---|---|---|---|---|')
    for n, cmd, v0, t, dist, stays, ok in rows:
        print(f'| {n} | {cmd:+.2f} | {v0:.3f} | '
              f'{"%.0f" % (t * 1000) if t is not None else "-"} | {dist * 100:.1f} | '
              f'{"yes" if stays else "no"} | {"PASS" if ok else "FAIL"} |')
    passed = sum(r[-1] for r in rows)
    print(f'\n{passed}/{len(rows)} runs passed')
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
