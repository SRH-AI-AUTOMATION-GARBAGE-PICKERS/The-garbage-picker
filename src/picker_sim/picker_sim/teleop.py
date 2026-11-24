"""Hold-to-drive keyboard teleop for the Picker's mecanum base.

Keys (hold; release = stop):
  I / K   forward / backward        (+x / -x)
  J / L   strafe left / right       (+y / -y), no rotation
  U / O   turn in place left / right (+wz / -wz, CCW / CW)
Keys combine: I+J drives diagonally, I+U drives an arc.

A Qt window is used instead of the terminal because a terminal only sees key
repeats, not key releases. The window must have focus. Losing focus stops
the robot.

Publishes geometry_msgs/Twist on /controller/cmd_vel at 20 Hz (zeros when no
key is held). The real ClawPi controller maps linear.x, linear.y, angular.z
through its mecanum kinematics, so this runs unchanged on the robot.

Speeds default to 50 % of SR-05 (SR-23: new motion code at 50 % limits) and
are clamped to the SR-05 limits whatever the parameters say:
  ros2 run picker_sim teleop --ros-args -p linear_speed:=0.3 -p angular_speed:=1.0
"""
import math
import signal
import sys

import rclpy
from geometry_msgs.msg import Twist
from rclpy.signals import SignalHandlerOptions
from python_qt_binding.QtCore import Qt, QTimer
from python_qt_binding.QtGui import QFont
from python_qt_binding.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

# SR-05 hard limits. Not parameters, so they can't be raised from the CLI.
MAX_LINEAR = 0.3   # m/s
MAX_ANGULAR = 1.0  # rad/s
RATE_HZ = 20.0

# key -> (x, y, wz) unit direction
KEYMAP = {
    Qt.Key_I: (1, 0, 0),
    Qt.Key_K: (-1, 0, 0),
    Qt.Key_J: (0, 1, 0),
    Qt.Key_L: (0, -1, 0),
    Qt.Key_U: (0, 0, 1),
    Qt.Key_O: (0, 0, -1),
}

HELP = (
    'Hold keys to drive (window must have focus)\n\n'
    '      I              U  turn left\n'
    '   J  K  L           O  turn right\n\n'
    'I/K fwd/back   J/L strafe   U/O turn in place'
)


class TeleopWindow(QWidget):

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.pressed = set()

        lin = node.declare_parameter('linear_speed', 0.5 * MAX_LINEAR).value
        ang = node.declare_parameter('angular_speed', 0.5 * MAX_ANGULAR).value
        self.linear = min(abs(lin), MAX_LINEAR)
        self.angular = min(abs(ang), MAX_ANGULAR)
        if self.linear != abs(lin) or self.angular != abs(ang):
            node.get_logger().warn(
                f'Speed clamped to SR-05: {self.linear} m/s, {self.angular} rad/s')
        node.get_logger().info(
            f'linear {self.linear} m/s, angular {self.angular} rad/s')

        self.pub = node.create_publisher(Twist, '/controller/cmd_vel', 10)

        self.setWindowTitle('Picker teleop')
        help_label = QLabel(HELP)
        help_label.setFont(QFont('Monospace', 10))
        self.status = QLabel()
        self.status.setFont(QFont('Monospace', 11))
        layout = QVBoxLayout(self)
        layout.addWidget(help_label)
        layout.addWidget(self.status)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(int(1000 / RATE_HZ))

    def command(self):
        x = sum(KEYMAP[k][0] for k in self.pressed)
        y = sum(KEYMAP[k][1] for k in self.pressed)
        wz = sum(KEYMAP[k][2] for k in self.pressed)
        # Normalise so a diagonal moves at linear_speed, not 1.41x.
        norm = math.hypot(x, y)
        if norm > 0:
            x, y = x / norm, y / norm
        return x * self.linear, y * self.linear, wz * self.angular

    def tick(self):
        x, y, wz = self.command()
        msg = Twist()
        msg.linear.x = float(x)
        msg.linear.y = float(y)
        msg.angular.z = float(wz)
        self.pub.publish(msg)
        self.status.setText(f'vx {x:+.2f}  vy {y:+.2f} m/s   wz {wz:+.2f} rad/s')
        rclpy.spin_once(self.node, timeout_sec=0)

    def keyPressEvent(self, event):
        if event.key() in KEYMAP and not event.isAutoRepeat():
            self.pressed.add(event.key())
            self.tick()

    def keyReleaseEvent(self, event):
        if event.key() in KEYMAP and not event.isAutoRepeat():
            self.pressed.discard(event.key())
            self.tick()

    def focusOutEvent(self, event):
        # Release events go to the other window, so stop here.
        self.pressed.clear()
        self.tick()

    def stop(self):
        if not self.timer.isActive():
            return
        self.pressed.clear()
        self.timer.stop()
        self.pub.publish(Twist())


def main():
    # Own signal handling: rclpy's handler would invalidate the context before
    # the final zero Twist is published.
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
    node = rclpy.create_node('picker_teleop')
    app = QApplication(sys.argv)
    win = TeleopWindow(node)
    win.setFocusPolicy(Qt.StrongFocus)
    win.show()
    for sig in (signal.SIGINT, signal.SIGTERM):  # Ctrl+C / kill in the terminal
        signal.signal(sig, lambda *_: app.quit())
    app.aboutToQuit.connect(win.stop)
    try:
        app.exec_()
    finally:
        win.stop()
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
