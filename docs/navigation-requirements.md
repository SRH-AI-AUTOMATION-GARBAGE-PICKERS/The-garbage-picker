# Picker: Navigation Requirements v0.1

| | |
|---|---|
| **Robot** | Picker, Hiwonder ClawPi Ultimate Kit (Raspberry Pi 5, 4× Mecanum drive, 2D LiDAR, monocular camera on pan-tilt, arm + gripper) |
| **Course** | AI and Autonomous Systems Lab, SRH Leipzig |
| **Author** | Developer / Safety Specialist |
| **Version** | 0.1 draft, 2026-11-24, for team review |
| **Related** | `docs/safety-requirements.md` (Safety Requirements v0.1, SR-xx IDs) |
| **Diagram** | `docs/img/picker-nav-example-route.svg` |

## 1. Scope

Picker has to drive from wherever it is to a pickup pose next to an ordered cube, and from there to the drop zone, without hitting or driving over anything. Product brief: "Scout finds, picker fetches." Cube detection, the picture-vs-real-cube decision and the grasp itself are out of scope here; this document covers only base motion between poses.

Picker has a 2D LiDAR and a monocular 480p camera, no depth sensor. It sees anything that cuts its LiDAR scan plane and nothing below it. Cubes and other low objects on the floor are below that plane, so Picker depends on Scout's depth camera for them.

All coordinates, the arena layout and every value marked *(hyp.)* are hypothetical and have to be replaced by measured values once the robot and arena are available (S4).

## 2. Robot facts that drive the design

| Item | Picker (ClawPi) | Scout (MentorPi A1) |
|---|---|---|
| Drive | Mecanum, holonomic: `vx`, `vy`, `wz` | Ackermann, car-like steering |
| Size | 313.5 × 170 × 170 mm (vendor, Ultimate Kit) | 213 × 159 × 157 mm (vendor, depth-camera version) |
| Circumscribed radius | 0.18 m (half-diagonal of 313.5 × 170 mm) | 0.13 m |
| Range sensor | 2D ToF LiDAR, 360° | 2D LiDAR (STL-19P) + 3D depth camera, 0.2–4 m depth range |
| Camera | Monocular 480p, pan-tilt | Depth camera (RGB + depth + point cloud) |
| ROS | ROS 2 Humble | ROS 2 Humble |

Speed and zone limits come from Safety Requirements v0.1 and are not redefined here: base ≤ 0.3 m/s linear, ≤ 1.0 rad/s angular (SR-05); slow to 0.1 m/s inside 1.0 m, stop inside 0.4 m of the robot outline (SR-06); command watchdog 500 ms (SR-03); stopping distance ≤ 0.15 m from 0.3 m/s (SR-13); floor-only operation in a marked area (SR-10).

## 3. Required navigation inputs

| ID | Input | Source | ROS interface | Freshness | Needed for |
|---|---|---|---|---|---|
| NI-01 | Static map of the arena | Built once with `slam_toolbox` (Picker or Scout LiDAR), saved, same file loaded on both robots | `nav_msgs/OccupancyGrid` on `/map`, frame `map` | Static per arena layout | Global planning, localization |
| NI-02 | Picker pose in `map` | AMCL on Picker (LiDAR + odometry) | TF `map → odom` | ≥ 10 Hz | Everything below |
| NI-03 | Wheel odometry | ClawPi base driver (encoders) | `nav_msgs/Odometry` on `/odom`, TF `odom → base_link` | ≥ 20 Hz | Local control, AMCL |
| NI-04 | LiDAR scan | Picker LiDAR driver | `sensor_msgs/LaserScan` on `/scan` | Sensor rate | Costmaps, AMCL, Collision Monitor |
| NI-05 | Target cube pose | Scout | `CubeTargetArray` (proposed, §8) on `/scout/cube_targets`, frame `map` | Per detection, stamped | Approach pose |
| NI-06 | Low obstacles | Scout | `LowObstacleArray` (proposed, §8) on `/scout/low_obstacles`, frame `map`, 1 Hz heartbeat | Full list every 1 s | Low-obstacle avoidance (§6) |
| NI-07 | Scout pose | Scout AMCL | `geometry_msgs/PoseStamped` on `/scout/pose`, frame `map` | ≥ 5 Hz | Treat Scout as moving obstacle |
| NI-08 | Drop zone pose | Static config | YAML parameter, frame `map` | Static | Drop goal |
| NI-09 | Arena boundary | Static config (tape is invisible to the LiDAR) | Polygon in YAML, rendered into the keepout mask | Static | Virtual walls |
| NI-10 | Order / mission | Operator or Scout | `PickOrder` (proposed) on `/picker/order`: cube ID to fetch | Per order | Mission state machine |
| NI-11 | Footprint and limits | Safety Requirements v0.1 | Nav2 parameters | Static | Planner, controller, Collision Monitor |

Picker publishes `/picker/pose` and `/picker/status` back to Scout so Scout can keep clear of it.

## 4. Coordinates and waypoints

### 4.1 Frames

One shared `map` frame for both robots, following REP 105 (`map → odom → base_link → laser`). The map origin is a taped corner marker of the arena; +x runs along the long arena edge, +y to the left of it, yaw counter-clockwise from +x. Both robots localize against the same map file, so a coordinate published by Scout means the same point for Picker without any transform between robots.

### 4.2 Pose types

| Pose | Definition |
|---|---|
| Approach pose `A` | Pose from which the arm reaches the cube without base motion: `A = (x_c − d·cos θ, y_c − d·sin θ, θ)`, with cube position `(x_c, y_c)`, approach heading `θ`, and `d` = distance from `base_link` to the grasp point, 0.30 m *(hyp., measure)* |
| Approach heading `θ` | Picked from 0°, 90°, 180°, 270°: the first candidate whose approach pose is free in the global costmap and closest to the robot. Mecanum drive allows the last few cm of lateral alignment without turning |
| Drop pose `D` | Fixed pose in front of the drop zone, from config (NI-08) |
| Home pose `H` | Fixed parking pose, from config |
| Via-waypoint `W` | Optional fixed pass-through point, only when a route has to follow a set corridor |

### 4.3 How Picker uses them

The default is one Nav2 goal per leg: `NavigateToPose` to `A`, grasp, `NavigateToPose` to `D`, release. The global planner picks the route through the costmap; waypoints `W` in the diagram are where that route bends, not hand-set targets. If the team wants a fixed corridor (for example, to stay out of Scout's search area), the leg uses `NavigateThroughPoses` with the `W` points listed.

Mission sequence, run as a small state machine on Picker:

```
IDLE → (order received) → PLAN_APPROACH → GO_TO_APPROACH → ALIGN → GRASP
     → GO_TO_DROP → RELEASE → (next order ? PLAN_APPROACH : GO_HOME) → IDLE
any state → (goal failed twice / watchdog / e-stop) → STOPPED, wait for operator
```

## 5. ROS 2 navigation concepts (Humble / Nav2)

| Function | Package / plugin | Setting for Picker |
|---|---|---|
| Map building | `slam_toolbox` (online async) | Once per arena layout; save with `nav2_map_server` |
| Map serving | `nav2_map_server` | Same map YAML on Picker and Scout |
| Localization | `nav2_amcl` | `robot_model_type: "nav2_amcl::OmniMotionModel"` (Mecanum strafes, so the differential model is wrong) |
| Global planner | `nav2_smac_planner/SmacPlanner2D` | Holonomic robot, so a 2D grid planner is enough; `allow_unknown: true` |
| Local controller | `nav2_mppi_controller` | `motion_model: "Omni"`, `vx_max: 0.3`, `vx_min: -0.3`, `vy_max: 0.3`, `wz_max: 1.0` (SR-05) |
| Velocity smoothing | `nav2_velocity_smoother` | Between controller and Collision Monitor |
| Reactive safety layer | `nav2_collision_monitor` | SR-06 zones on `/scan`. Humble supports `stop`, `slowdown`, `approach` and uses `max_points` (default 3, so 4 points trigger) instead of the later `min_points` |
| Virtual obstacles | Costmap filter `nav2_costmap_2d::KeepoutFilter` + `nav2_map_server` costmap filter info server | One mask that holds the arena boundary band and Scout's low obstacles (§6) |
| Speed limit on stale data | Controller server `speed_limit` topic (`nav2_msgs/SpeedLimit`) | Drop to 0.1 m/s when Scout data is stale (§6, step 5) |
| Behavior tree | `nav2_bt_navigator` | `NavigateToPose`, `NavigateThroughPoses` |
| Cross-robot topics | `domain_bridge` (Humble release 0.5.0) | Whitelist of topics between Scout and Picker domains (§8), keeps SR-31 domain separation |

Command chain: `controller_server → velocity_smoother → collision_monitor → base driver`. The base driver keeps the SR-03 watchdog, so a crashed Nav2 node or Wi-Fi drop stops the wheels within 500 ms regardless of what Nav2 does.

Costmap layers:

- Global costmap: static layer (NI-01), obstacle layer (`/scan`), keepout filter, inflation layer.
- Local costmap: rolling window 3 × 3 m, obstacle layer (`/scan`), keepout filter, inflation layer.

## 6. Obstacle handling

### 6.1 Obstacle classes and challenges

| # | Obstacle / challenge | Why it is a problem for Picker | Handling |
|---|---|---|---|
| OB-1 | Low objects (cubes, blocks, cables) with top below the LiDAR scan plane | Invisible to every Picker sensor used for navigation | Scout-reported mask (§6.2) |
| OB-2 | Non-target cubes | Also low, also invisible; the brief forbids driving over them | Scout reports every cube; all but the target go into the mask |
| OB-3 | The target cube itself | If it stays in the mask, the approach pose sits inside a lethal cell and planning fails | Target cube is removed from the mask while it is the active goal |
| OB-4 | Printed pictures of cubes on the floor | Flat, so not an obstacle; also not a target | Scout classifies them and leaves them out of both lists; Picker may drive over them (assumption AS-07) |
| OB-5 | Tall static objects (boxes, chair legs, walls) | Seen by LiDAR, but SR-06 stops Picker inside 0.4 m of its outline | Normal obstacle layer; arena layout keeps passages ≥ 1.0 m wide (§7, AS-05) |
| OB-6 | Scout | Moving; may also be low enough to pass under the scan plane in parts | Scout pose (NI-07) drawn as a 0.13 m radius disc into the mask, plus LiDAR |
| OB-7 | Persons | Moving, unpredictable | LiDAR + Collision Monitor (SR-06); the planner does not try to predict them |
| OB-8 | Overhangs (table tops above the scan plane) | Invisible, but only hit the 170 mm tall robot or its raised arm | Not allowed in the arena (AS-06) |
| OB-9 | Stale Scout data | An obstacle moved after Scout last saw it | Heartbeat, speed limit, re-scan request (§6.2, step 5) |
| OB-10 | Map offset between robots | Each robot's AMCL error adds to the obstacle position error | 0.10 m localization margin in the mask radius |
| OB-11 | Black or reflective surfaces | ToF LiDAR returns drop out, obstacle looks like free space | Matte arena objects (AS-08) |
| OB-12 | Mecanum wheel slip | Odometry drifts, especially when strafing | AMCL correction; no long strafes outside LiDAR-visible features |

### 6.2 Strategy for low obstacles

1. **Definition.** A low obstacle is any object whose top is below Picker's LiDAR scan plane height `h_scan`, 0.12 m *(hyp., measure from floor to the LiDAR optical centre)*.
2. **Detection on Scout.** Scout's depth camera (0.2–4 m depth range) detects low objects, converts them to the `map` frame with its own AMCL pose and publishes the full list on `/scout/low_obstacles` once per second, also when nothing changed. Each entry carries position, radius `r_obs` and height. Scout sweeps the whole arena once before Picker gets its first order (AS-03).
3. **Mask on Picker.** A Picker-side node (`scout_obstacle_mask`) turns the list into an `OccupancyGrid` with the same resolution and origin as the static map: cells inside a disc of radius `r = r_obs + 0.18 m (footprint) + 0.10 m (localization margin)` get value 100, the rest 0. The arena boundary band (0.28 m inside the tape) is burned into the same mask. The node publishes on `/keepout_filter_mask` with transient-local QoS.
4. **Why pre-inflate.** Costmap filters are not inflated by the inflation layer, so the footprint and margin have to be in the mask already. The Humble `KeepoutFilter` replaces the old mask completely when a new one arrives, so obstacles Scout removes from its list also leave Picker's costmap on the next update.
5. **Stale data.** If no list arrives for 5 s, Picker publishes a 0.1 m/s speed limit, keeps the last mask, starts no new leg and asks Scout for a re-scan. Normal speed comes back with the next list.
6. **Target exclusion.** The mask node gets the active target cube ID from the mission state machine and leaves that cube out of the mask. Every other cube stays in.
7. **Collision Monitor stays LiDAR-only.** Scout data arrives over Wi-Fi with up to 1 s of age; that is fine for planning, not for the reactive stop. The SR-06 stop/slowdown decision uses `/scan` only.

## 7. Example scenario

![Picker example route](img/picker-nav-example-route.svg)

Arena 4.0 × 3.0 m, tape boundary, map origin at the bottom-left corner. Order: fetch cube C1, deliver to the drop zone.

| Element | Position `(x, y)` [m] | Notes |
|---|---|---|
| Start `S` | (0.50, 0.50), yaw 0° | Picker home |
| Target cube C1 | (1.50, 2.40) | From `/scout/cube_targets` |
| Approach pose A1 | (1.50, 2.10), yaw 90° | `d = 0.30 m`, 90° is the closest free candidate to `S` (1.89 m; 0° gives 2.02 m, 180° gives 2.30 m) |
| Drop pose `D` | (3.00, 2.43), yaw 0° | Config; drop zone tape square 3.25–3.70 × 2.20–2.65 |
| L1 (low block) | (0.80, 1.00), `r_obs` 0.04 | Mask radius 0.32 m |
| L2 (low block) | (2.25, 2.25), `r_obs` 0.04 | Mask radius 0.32 m |
| C2 (other cube) | (3.30, 0.60), `r_obs` 0.04 | In mask because it is not the target |
| P (cube picture) | (1.15, 0.45) | Not in either list |
| T1 (box, 0.6 × 0.6 m) | 2.0–2.6 × 0.5–1.1 | LiDAR-visible |
| Scout | (3.50, 1.30) | From `/scout/pose` |

Sequence:

1. Order arrives. Picker computes A1 from C1 and sends `NavigateToPose(A1)`.
2. The straight line `S → A1` passes 0.02 m from L1, deep inside its 0.32 m mask. The planner routes east of L1 through W1 (1.40, 0.75); closest approach to L1 is 0.40 m, so the route stays outside the mask. On the `W1 → A1` stretch `base_link` stays ≥ 0.57 m from T1, so the outline stays ≥ 0.41 m away even with the long side facing the box: outside the 0.4 m stop zone but inside the 1.0 m slowdown zone, so Picker runs at 0.1 m/s on that stretch.
3. At A1 the controller aligns to 90°; the ALIGN state corrects the last cm laterally. Picker grasps C1. Scout's next obstacle list no longer contains C1 because it is in the gripper, so nothing has to be added back to the mask.
4. `NavigateToPose(D)`. The direct line passes through L2's mask, and passing south of L2 is limited by T1. The planner goes through W2 (2.30, 1.78), 0.47 m from L2 and 0.68 m above T1, then W3 (2.85, 2.10) to `D`.
5. If Scout drives into the route, it shows up in the mask (NI-07) and in `/scan`; the controller replans around it, or the Collision Monitor stops Picker at 0.4 m if Scout comes too close too fast.
6. At `D` Picker releases C1, reports `/picker/status = DELIVERED` and returns to IDLE.

## 8. Interface with Scout

Proposed for the inter-team interface contract (message package `warehouse_interfaces`, name to be agreed with team Scout):

```
# LowObstacle.msg
string id
geometry_msgs/Point position     # map frame, z = 0
float32 radius                   # m, circumscribed radius of the object footprint
float32 height                   # m

# LowObstacleArray.msg
std_msgs/Header header           # frame_id: map, stamp = time of the sweep
LowObstacle[] obstacles          # full list, not a delta

# CubeTarget.msg
string cube_id
string color
geometry_msgs/Pose pose          # map frame
float32 confidence               # 0..1
bool is_physical                 # false = picture, never sent as target

# CubeTargetArray.msg
std_msgs/Header header
CubeTarget[] cubes
```

Domain bridge config (domain IDs hypothetical, one per team per SR-31):

```yaml
name: scout_picker_bridge
from_domain: 11   # Scout
to_domain: 12     # Picker
topics:
  scout/low_obstacles:
    type: warehouse_interfaces/msg/LowObstacleArray
  scout/cube_targets:
    type: warehouse_interfaces/msg/CubeTargetArray
  scout/pose:
    type: geometry_msgs/msg/PoseStamped
  picker/pose:
    type: geometry_msgs/msg/PoseStamped
    reversed: true
  picker/status:
    type: std_msgs/msg/String
    reversed: true
```

Only these five topics cross between domains; `cmd_vel` and all actuator topics never do.

## 9. Assumptions

| ID | Assumption |
|---|---|
| AS-01 | Scout is the depth-camera version of the MentorPi A1 and runs AMCL on the same map file as Picker |
| AS-02 | Each robot's AMCL position error is ≤ 0.05 m, and Scout's obstacle position error is ≤ 0.05 m; together this is the 0.10 m margin *(hyp., measure in S4)* |
| AS-03 | Scout completes one full sweep of the arena before the first order |
| AS-04 | The floor is flat; Picker never has to drive over anything |
| AS-05 | Passages between LiDAR-visible objects are ≥ 1.0 m wide (0.17 m robot width + 2 × 0.4 m SR-06 stop zone = 0.97 m) |
| AS-06 | No overhanging objects in the arena |
| AS-07 | Cube pictures are flat paper taped to the floor and can be driven over |
| AS-08 | Arena objects are matte enough for the ToF LiDAR |
| AS-09 | The drop zone is tape on the floor, not a bin with walls above the scan plane |
| AS-10 | Arena 4.0 × 3.0 m, hypothetical; all coordinates in this document are examples |

## 10. Limitations

- Picker cannot detect low obstacles on its own. If Scout misses one, Picker drives into it; the 0.1 m/s stale-data limit reduces the impact but does not prevent it.
- Obstacle information is up to 1 s old (heartbeat period) plus Wi-Fi latency. Moving low objects are not handled.
- The 1.0 m slowdown zone in SR-06 cannot tell a person from a box, so Picker drives at 0.1 m/s whenever any LiDAR-visible object is within 1.0 m. In a 4 × 3 m arena that covers much of the route.
- The SR-06 0.4 m stop zone blocks approach to any LiDAR-visible object closer than 0.4 m, so a drop bin with walls (AS-09 not holding) needs a separate low-speed docking mode.
- One shared map means a layout change (moved box) needs a re-map or the static layer will disagree with the scan until the obstacle layer clears it.

## 11. Open items

| # | Item | Owner | Action |
|---|---|---|---|
| NO-1 | `h_scan`: LiDAR scan plane height above floor | Picker dev | Measure on the robot |
| NO-2 | `d`: `base_link` to grasp point distance | Picker arm dev | Measure with arm in grasp pose |
| NO-3 | Message definitions and topic names (§8) | Both POs | Put into the interface contract |
| NO-4 | Domain IDs and bridge host (Picker Pi or a laptop) | Both teams | Agree and add to SR-31 |
| NO-5 | Drop zone design (tape or bin) | PO / customer | Ask the customer; if bin, define docking mode with Safety |
| NO-6 | Localization and detection error (AS-02) | Both teams | Measure in S4, then adjust the 0.10 m margin |
| NO-7 | Slowdown zone vs. throughput (§10) | Safety | Decide whether SR-06 slowdown applies to all LiDAR objects or only near unknown/moving ones |

## 12. Review record

| Reviewer | Role | Date | Result | Evidence (PR / comment link) |
|---|---|---|---|---|
| | | | | |

## Sources

1. Course session sheet S1, product brief: https://courses.timgarbe.de/ai-and-autonomous-systems-lab/lectures/s1-team-building-and-scrum-setup-session-sheet.html
2. Picker Safety Requirements v0.1 (this repository), SR-03, SR-05, SR-06, SR-10, SR-13, SR-31.
3. ClawPi dimensions (313.5 × 170 × 170 mm, Ultimate Kit) and sensors: https://thinkrobotics.com/products/clawpi-ros2-ai-robot-car-raspberry-pi-5-mecanum-robot and https://openelab.io/products/hiwonder-clawpi-ros2-robot
4. MentorPi A1 depth-camera version, size and sensors: https://hiwonder.com/products/mentorpi-a1 ; depth range 0.2–4 m: https://cnx-software.com/2024/10/23/mentorpi-is-a-ros2-compatible-raspberry-pi-5-based-robot-car-with-mecanum-or-ackermann-chassis
5. Nav2 MPPI controller, Humble package and Omni motion model: https://docs.ros.org/en/humble/p/nav2_mppi_controller/ , https://docs.nav2.org/configuration/packages/configuring-mppic.html
6. AMCL `OmniMotionModel` in Humble: https://docs.ros.org/en/humble/p/nav2_amcl/generated/classnav2__amcl_1_1OmniMotionModel.html
7. Keepout filter configuration and Humble source (mask replacement, no inflation): https://docs.nav2.org/configuration/packages/costmap-plugins/keepout_filter.html , https://api.nav2.org/nav2-humble/html/keepout__filter_8cpp_source.html
8. Collision Monitor configuration (`max_points` in Humble): https://docs.nav2.org/configuration/packages/collision_monitor/configuring-collision-monitor-node.html
9. `domain_bridge` for Humble: https://index.ros.org/r/domain_bridge
