# Scout–Picker Communication

This page collects what the Picker (our ClawPi) needs from the Scout robot (Team Scout's MentorPi A1), the customer's answers, our open questions, and our **proposed interface** for discussion with Team Scout.

> **Status:** draft v0.1, Sprint 3. Not agreed with Team Scout yet. Once both teams agree, the "Interface proposal" part is copied to `docs/interface-contract.md` as **v1** (see [[Workflow]] §10). Items marked **(assumption)** are not confirmed.

Issues: #18 Identify initial Scout–Picker communication requirements · Propose Picker–Scout interface

## Summary

Customer brief: *"On an order, I want the robots to find the ordered cubes and bring them to the drop zone, without driving over anything and without being fooled by pictures. Scout finds, picker fetches."*

| Question | Answer |
|---|---|
| What does one order contain? | One cube, identified by its colour |
| How many orders at once? | One. A new order is rejected while one is running |
| Who finds the cube? | Scout |
| Who picks it up and delivers it? | Picker |
| How do the robots talk? | ROS 2 topics + one action (details below) |
| Where does the MVP run? | In simulation, all steps from order to delivery |

## Customer answers (Sprint 3)

Asked by our team, answered by the customer (Tim).

| # | Question | Answer | What it means for us |
|---|---|---|---|
| 1 | Will you place orders? | Yes, orders | We need an "order" input |
| 2 | What differs between orders? | Always pick up and deliver. The cube (colour) changes | An order = one colour |
| 3 | Can one order contain multiple cubes? | One cube per order | No count field needed |
| 4 | Can a new order arrive while one is processed? | No queue, one order at a time | Reject new orders while busy |
| 5 | What if a cube isn't found? | Information is displayed | The user must see a "not found" message |
| 6 | Should the user see the order status? | Yes (some kind of response) | Order status messages |
| 7 | Marking | Not important | Not part of the interface |
| 8 | Can cubes be moved while the robots work? | Cubes always stay in the same place | Scout's position stays valid; no live updates needed |
| 9 | Obstacle in the way: move it? | If there's no way around it, skip | Error "path blocked" → order skipped, user informed |
| 10 | Speed or success? | Successful delivery is more important than speed | Slow and careful is fine; retries are fine |
| 11 | Dropped cube: failure or retry? | It can be picked up again | Picker retries the pickup |
| 12 | What should the first MVP show? | The robot doing all steps in simulation | MVP target: full flow in Gazebo |

## The words we use

| Word | Meaning |
|---|---|
| Order | A request from the user: "bring me the **red** cube" |
| Scout | Team Scout's robot (MentorPi A1). Finds cubes |
| Picker | Our robot (ClawPi). Picks up the cube and delivers it |
| Cube | The object to collect (probably the kit's 35 mm EVA colour blocks) **(assumption)** |
| Drop zone | Where the Picker delivers the cube |
| Task | Scout's instruction to the Picker: "pick cube X, bring it to the drop zone" |
| Frame | A coordinate system, e.g. "position (1.2, 0.5) in the `map` frame" |

## Requirements

### What the Picker needs from Scout

| # | Information | Why | Priority |
|---|---|---|---|
| 1 | Position of the ordered cube (x, y; z ≈ 0) | To drive to it and grab it | Must |
| 2 | Cube ID | To refer to the same cube in tasks and results | Must |
| 3 | The coordinate frame and its origin | Positions are meaningless without it | Must |
| 4 | Confirmation that the cube is a real 3D object, not a picture | Customer: "not fooled by pictures" | Must |
| 5 | Drop zone position and size | To know where to deliver | Must |
| 6 | The task (which cube, which order) | So both robots work on the same order | Must |
| 7 | Scout's position | Avoid collisions | Should |
| 8 | Position accuracy (± cm) | How far around the position the Picker must search | Should |

### What Scout needs from the Picker

| # | Information | Why | Priority |
|---|---|---|---|
| 1 | Task accepted / rejected | Scout knows the job was received | Must |
| 2 | Current step (driving, picking, carrying, delivering) | Order status for the user | Must |
| 3 | Result: delivered / failed + reason | Final order status for the user | Must |
| 4 | Picker position | Avoid collisions | Should |

### What the user needs

| # | Information | Why | Priority |
|---|---|---|---|
| 1 | A way to place an order (choose a colour) | Customer answers 1–2 | Must |
| 2 | "Order accepted" or "busy, try later" | One order at a time (answer 4) | Must |
| 3 | Order status while it runs | Answer 6 | Must |
| 4 | A clear message when the cube isn't found or the order is skipped | Answers 5 and 9 | Must |

## Feature: order fulfilment

Written with our [[Development Guidelines — Specs, Modularity & ADRs]] template.

### Rules

- Only one order at a time. While an order runs, new orders are rejected.
- One order = one cube of one colour.
- Only cubes confirmed as real 3D objects may be assigned to the Picker.
- Scout sends tasks, never movement commands. Only the Picker's own controller moves the Picker (safety limits SR-03 and the speed limits stay with the Picker).
- Successful delivery is more important than speed.
- Every order ends with a final status the user can see: `DELIVERED`, `NOT_FOUND`, `SKIPPED` or `FAILED`.
- All positions are in metres, in the shared `map` frame.

### Inputs

- The order: a colour, from the user.
- Scout's detections of cubes and their positions.
- The drop zone position.
- Robot positions (Scout and Picker).
- Current state: is an order already running?

### Normal flow

1. The user places an order for one colour.
2. The order is accepted, status `RECEIVED`.
3. Scout searches for a cube of that colour, status `SEARCHING`.
4. Scout finds it and confirms it's a real 3D cube, status `CUBE_FOUND`.
5. Scout sends the task to the Picker (cube ID, cube position, drop zone).
6. The Picker drives to the cube, status `PICKER_DRIVING`.
7. The Picker grabs the cube, status `PICKING`.
8. The Picker drives to the drop zone, status `CARRYING`.
9. The Picker releases the cube in the drop zone.
10. The Picker reports success, final status `DELIVERED`. A new order can be placed.

### Outputs

- Order status messages for the user at every step.
- The cube is in the drop zone.
- Both robots are idle and ready for the next order.

### Branches

| If… | Then… | Final status |
|---|---|---|
| A new order arrives while one is running | Reject it with "busy, one order at a time" | (first order continues) |
| Scout finds no cube of that colour | Show "cube not found" to the user | `NOT_FOUND` |
| Scout only finds a picture of a cube | Treat it as not found | `NOT_FOUND` |
| The Picker finds nothing at the given position | Search a small area around it; if still nothing, report to Scout; Scout re-checks once | `NOT_FOUND` if still missing |
| Grasp fails or the cube is dropped | Pick it up again, up to 3 tries **(proposal)** | `FAILED` after 3 failed tries |
| An obstacle blocks the way and there's no way around | Skip the order and tell the user why | `SKIPPED` |
| A person or object comes within 0.4 m | Stop (safety rule), continue when clear | (no change) |
| The connection between the robots is lost | The Picker stops (watchdog, SR-03) | `FAILED` |
| Battery too low to finish | The Picker rejects the task | `FAILED` |

## Interface proposal (v0.1)

### Overview

| What | Direction | ROS 2 type | Name |
|---|---|---|---|
| Place an order | User → Scout **(assumption)** | Service | `/order/place` |
| Order status | Scout → User | Topic | `/order/status` |
| Found cubes | Scout → Picker | Topic | `/scout/cubes` |
| Drop zone | Scout → Picker | Topic (latched) | `/scout/drop_zone` |
| Scout position | Scout → Picker | Topic | `/scout/pose` |
| Pickup task | Scout → Picker | Action | `/picker/pick_and_deliver` |
| Picker status | Picker → Scout | Topic | `/picker/status` |
| Picker position | Picker → Scout | Topic | `/picker/pose` |

```
 User ──/order/place──► ┌────────┐ ──/scout/cubes, /scout/drop_zone, /scout/pose──► ┌────────┐
      ◄─/order/status── │ Scout  │ ──/picker/pick_and_deliver (action goal)───────► │ Picker │
                        │        │ ◄─action feedback + result, /picker/status,───── │(ClawPi)│
                        └────────┘    /picker/pose                                  └────────┘
```

All custom definitions go in one shared package, `scout_picker_interfaces`.

### Coordinate system and units

| Rule | Value |
|---|---|
| Units | metres, radians, seconds ([REP 103](https://www.ros.org/reps/rep-0103.html)) |
| Axes | x forward, y left, z up, right-handed ([REP 103](https://www.ros.org/reps/rep-0103.html)) |
| Shared world frame | `map` ([REP 105](https://www.ros.org/reps/rep-0105.html)) |
| Robot frames | `scout/base_footprint`, `picker/base_footprint` (as in our Picker sim) |
| Rotation | quaternion in poses |
| Time | `header.stamp` in every message |

Origin of `map`, proposal: one marked corner of the warehouse is (0, 0, 0), x along one wall, y along the other. To agree with Team Scout.

Every position must have `header.frame_id`. A message without it is invalid.

### Order service: `/order/place`

Type `scout_picker_interfaces/srv/PlaceOrder`.

```
# Request
string color                 # e.g. "red"
---
# Response
bool accepted
string order_id              # e.g. "order_004"; "" if rejected
string message               # e.g. "busy, one order at a time"
```

### Order status: `/order/status`

Type `scout_picker_interfaces/msg/OrderStatus`. Published on every change. Reliable, transient local (a screen started late still shows the last status).

```
std_msgs/Header header
string order_id
string color
uint8 state
uint8 RECEIVED       = 0
uint8 SEARCHING      = 1
uint8 CUBE_FOUND     = 2
uint8 PICKER_DRIVING = 3
uint8 PICKING        = 4
uint8 CARRYING       = 5
uint8 DELIVERED      = 6    # final
uint8 NOT_FOUND      = 7    # final
uint8 SKIPPED        = 8    # final
uint8 FAILED         = 9    # final
uint8 error_code            # see Errors
string message              # text shown to the user
```

### Found cubes: `/scout/cubes`

Type `scout_picker_interfaces/msg/CubeArray`. Cubes don't move (customer answer 8), so Scout publishes when it finds something new.

```
# Cube.msg
string id                         # stable, e.g. "cube_7"
geometry_msgs/PoseStamped pose    # centre of the cube, map frame
string color
float32 confidence                # 0.0–1.0
bool verified_3d                  # true = real object, not a picture
float32 position_accuracy         # metres (± radius)

# CubeArray.msg
std_msgs/Header header
Cube[] cubes
```

### Drop zone: `/scout/drop_zone`

Type `scout_picker_interfaces/msg/Zone`. Reliable, transient local.

```
geometry_msgs/PoseStamped center
float32 radius                    # metres
```

### Robot positions: `/scout/pose`, `/picker/pose`

Type `geometry_msgs/msg/PoseStamped` (standard). About 5× per second **(assumption)**.

### Picker status: `/picker/status`

Type `scout_picker_interfaces/msg/PickerStatus`. 1× per second and on every change.

```
std_msgs/Header header
uint8 state
uint8 IDLE       = 0
uint8 DRIVING    = 1
uint8 PICKING    = 2
uint8 CARRYING   = 3
uint8 RELEASING  = 4
uint8 STOPPED    = 5     # safety stop, waiting
uint8 ERROR      = 6
string order_id
uint8 error_code
string error_text
float32 battery          # 0.0–1.0, -1 if unknown
```

### Pickup task: action `/picker/pick_and_deliver`

Type `scout_picker_interfaces/action/PickAndDeliver`. The Picker is the action server; Scout is the client. One task at a time.

```
# Goal
string order_id
string cube_id
geometry_msgs/PoseStamped cube_pose
float32 search_radius             # metres, from Scout's accuracy
geometry_msgs/PoseStamped drop_pose
---
# Result
bool success
uint8 error_code
string message
uint8 attempts                    # grasp attempts used
---
# Feedback
uint8 stage                       # PickerStatus state values
float32 distance_to_target        # metres
uint8 attempt                     # current grasp attempt
```

Why an action: the job takes a long time, Scout needs progress for the user's order status, and it must be cancellable.

### Errors

| Code | Name | Meaning | Order status |
|---|---|---|---|
| 0 | `NONE` | All good | — |
| 1 | `CUBE_NOT_FOUND` | Nothing at the given position | `NOT_FOUND` |
| 2 | `GRASP_FAILED` | Couldn't hold the cube after 3 tries | `FAILED` |
| 3 | `PATH_BLOCKED` | No way around an obstacle | `SKIPPED` |
| 4 | `BUSY` | Already working on an order | (order rejected) |
| 5 | `INVALID_GOAL` | Missing frame or bad data | `FAILED` |
| 6 | `LOW_BATTERY` | Not enough battery | `FAILED` |
| 7 | `CONNECTION_LOST` | No messages from the other robot | `FAILED` |
| 8 | `CANCELLED` | Task cancelled | `FAILED` |

### Example messages

Place an order:

```bash
ros2 service call /order/place scout_picker_interfaces/srv/PlaceOrder "{color: red}"
```

```yaml
accepted: true
order_id: order_004
message: "Order received: red cube"
```

Order status the user sees when the cube isn't found:

```yaml
order_id: order_004
color: red
state: 7
error_code: 1
message: "No red cube found in the warehouse"
```

Task sent to the Picker:

```yaml
order_id: order_004
cube_id: cube_7
cube_pose:
  header: {frame_id: map}
  pose: {position: {x: 1.20, y: 0.50, z: 0.0}, orientation: {w: 1.0}}
search_radius: 0.10
drop_pose:
  header: {frame_id: map}
  pose: {position: {x: 0.20, y: 2.00, z: 0.0}, orientation: {w: 1.0}}
```

## Network and domains

| Setup | Domains | How the robots talk | Pickup task |
|---|---|---|---|
| **MVP: simulation** (customer answer 12) | One domain, everything prefixed `/scout/...`, `/picker/...` | Directly | Action, as above |
| **Real robots (from S4)** | **Different** `ROS_DOMAIN_ID` per robot (safety requirement SR-31), isolated Wi-Fi (SR-30) | `domain_bridge` forwards only the topics in this contract | Action replaced by two topics (`/scout/task`, `/picker/task_result`), because we found no action support in `domain_bridge` |

Example bridge configuration for the real robots:

```yaml
name: scout_picker_bridge
from_domain: 11        # Scout (example number)
to_domain: 12          # Picker (example number)
topics:
  scout/cubes:
    type: scout_picker_interfaces/msg/CubeArray
  scout/drop_zone:
    type: scout_picker_interfaces/msg/Zone
  scout/pose:
    type: geometry_msgs/msg/PoseStamped
  picker/status:
    type: scout_picker_interfaces/msg/PickerStatus
    from_domain: 12
    to_domain: 11
  picker/pose:
    type: geometry_msgs/msg/PoseStamped
    from_domain: 12
    to_domain: 11
```

The Picker's movement topic (`/controller/cmd_vel`) is never bridged. This decision needs an ADR (ADR-001).

## Open questions

### For the customer (via PO, label `question-for-customer`)

1. Where and how should information be "displayed": terminal, a screen on the robot (the ClawPi has a 1.9" LCD), or a web page?
2. Is there one drop zone or several? Is its position fixed and known?
3. Which colours can be ordered? Are the cubes the 35 mm EVA blocks from the kit?
4. Can two cubes of the same colour exist? If yes, which one should be picked?
5. Who places orders in the demo: a person typing a command, or something else?
6. What does "marking" refer to (answer 7), so we document it correctly?

### For Team Scout

1. Who receives the order: Scout, or a separate coordinator program?
2. How does Scout detect cubes, and how does it tell a real cube from a picture?
3. How accurate are Scout's positions (± cm)?
4. Which frame does Scout use? Do you agree with the `map` origin proposal?
5. Does Scout build a map it can share?
6. Do you agree with the action for the pickup task in simulation, and topics on the real robots?
7. Which ROS 2 version and `ROS_DOMAIN_ID` does Scout use? Who runs the `domain_bridge`?
8. Who owns the shared `scout_picker_interfaces` package?
9. For the MVP: do we run both robots in one shared Gazebo world?

## Assumptions (not confirmed)

- The order goes to Scout, which then gives the task to the Picker.
- There is one drop zone, at a fixed known position.
- Cubes lie on the floor (z ≈ 0).
- Cubes are the 35 mm EVA blocks from the kit.
- 3 grasp attempts before giving up.
- Both teams use ROS 2 Humble.

## Feedback from Team Scout

| Date | Who | Topic | Agreed / changed / open |
|---|---|---|---|
| _TBD_ | | | |

## Acceptance criteria

**#18 Identify initial Scout–Picker communication requirements**

- [x] Initial communication requirements are documented — Requirements
- [x] Open questions for the customer are listed — Open questions → customer
- [x] Questions for Team Scout are documented — Open questions → Team Scout
- [x] Unconfirmed assumptions are clearly identified — Assumptions
- [ ] Findings are committed to the repository

**Propose Picker–Scout interface**

- [x] Required information is identified — Requirements
- [x] Proposed message structures are documented — Interface proposal
- [x] Coordinate conventions and units are specified — Coordinate system and units
- [x] At least one valid example message is provided — Example messages
- [ ] Team Scout has reviewed the proposal, or outstanding coordination is documented — Feedback from Team Scout

## Sources

- [REP 103 — Standard Units of Measure and Coordinate Conventions](https://www.ros.org/reps/rep-0103.html)
- [REP 105 — Coordinate Frames for Mobile Platforms](https://www.ros.org/reps/rep-0105.html)
- [ROS 2 Humble — Understanding topics](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
- [ROS 2 Humble — Understanding services](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)
- [ROS 2 Humble — Understanding actions](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)
- [ROS 2 Humble — Creating custom msg and srv files](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html)
- [ROS 2 — Quality of Service settings](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
- [domain_bridge package](https://index.ros.org/p/domain_bridge)
- Team docs: README (customer brief), `docs/picker-safety-requirements.md` (SR-03, SR-30, SR-31), [[Workflow]] §10
