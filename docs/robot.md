# Hiwonder ClawPi Ultimate Kit --- Complete Parts Guide

> **Purpose:** A photo-friendly inventory of the parts supplied with the
> Hiwonder ClawPi Ultimate Kit. Each entry has a dedicated image
> placeholder. Replace the placeholder image paths with your own
> photographs.
>
> **Source:** [Hiwonder ClawPi User Manual --- sections 1.1 Getting to
> Know ClawPi and 1.2 Product
> Assembly](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-getting-to-know-clawpi)

# Official Robot/Part Pictures

If you need pictures of the ClawPi robot components, assembly parts,
or hardware details, please visit the official Hiwonder documentation:

🔗 [Hiwonder ClawPi User Manual](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-getting-to-know-clawpi)

The manual contains pictures, component descriptions, assembly
instructions, and wiring diagrams.

**Inventory note:** The manual lists some items as kits or sets (for
example, the chassis bracket set, cooling fan kit, and accessory pack)
without itemizing every screw, bracket, or sub-piece. Those entries are
kept as supplied-kit groups rather than guessing at their contents. The
Raspberry Pi 5 board is explicitly marked optional in the packing list.

------------------------------------------------------------------------

# 1. Standard robot components

The Ultimate Kit includes the Standard Kit components, plus the LiDAR
and robotic-arm expansion packs.

## 1.1 Robot chassis bracket set

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1 set

**What it is:** The structural frame and brackets that form the robot's
body and provide mounting points for the electronics, motors, battery,
sensors, and upper modules.

**What it does:** Holds the robot together and keeps the major
components in their intended positions.

**Where it belongs:** The main body/base of the robot.

## 1.2 Raspberry Pi 5 board (optional)

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1 (optional)

**What it is:** The robot's main single-board computer.

**What it does:** Runs the robot's software and higher-level functions.
The manual describes ClawPi as a Raspberry Pi-powered ROS robot.

**Where it belongs:** Mounted on the chassis using the supplied nylon
standoffs.

## 1.3 Raspberry Pi 5 expansion board

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1

**What it is:** The interface and control board used to connect the
robot's motors, servos, sensors, and power.

**What it does:** Provides the numbered connections used in the
manual: - No. 1 --- camera pan-tilt vertical-tilt servo - No. 2 ---
camera pan-tilt horizontal-pan servo - No. 3 --- robotic-arm lift
servo - No. 4 --- gripper servo - No. 5 --- LiDAR - No. 6 ---
four-channel line follower sensor - M1--M4 --- four drive motors

**Where it belongs:** Mounted above the chassis on nylon standoffs, with
the Raspberry Pi and other electronics connected as shown in the wiring
diagrams.

## 1.4 Cooling fan kit

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1 kit

**What it is:** The cooling hardware supplied for the
computer/electronics assembly.

**What it does:** Helps remove heat from the Raspberry Pi during
operation.

**Where it belongs:** Installed with the Raspberry Pi/heatsink assembly
as shown in the assembly instructions.

## 1.5 HD camera pan-tilt assembly

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1 assembly

**What it is:** The camera module mounted on a two-degree-of-freedom
(2DOF) pan-tilt mechanism.

**What it does:** Provides the robot with visual input. The two servos
let the camera tilt vertically and pan horizontally.

**Where it belongs:** On the upper part of the robot.

**Servo connections:** Servo No. 1 controls vertical tilt; Servo No. 2
controls horizontal pan.

## 1.6 Mecanum wheels

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 4 wheels

**What they are:** Special wheels with angled rollers around their
circumference.

**What they do:** Allow the robot to move in multiple directions,
including sideways movement, when driven by the four-wheel chassis.

**Where they belong:** One wheel on each of the four motor shafts. The
manual specifies: - Front-left: M1 - Rear-left: M2 - Front-right: M3 -
Rear-right: M4

## 1.7 Encoder motors

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 4 motors

**What they are:** Drive motors with encoders.

**What they do:** Turn the Mecanum wheels and provide rotation feedback
for motion control.

**Where they belong:** Inside the chassis, one at each wheel position.

**Motor labels in the manual:** - M1 --- front-left - M2 --- rear-left -
M3 --- front-right - M4 --- rear-right

Connect each motor cable to its matching numbered motor port.

## 1.8 Four-channel line follower sensor

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1

**What it is:** A sensor module with four line-detection channels.

**What it does:** Detects a line or track beneath the robot for
line-following activities.

**Where it belongs:** Under the front of the chassis. The manual says to
treat the side carrying this sensor as the front of the robot.

**Connection:** Connect its cable to the designated sensor port on the
Raspberry Pi expansion board (No. 6).

## 1.9 WonderEcho Pro AI voice interaction box

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1

**What it is:** The robot's AI voice-interaction module.

**What it does:** Adds voice interaction capabilities to ClawPi.

**Where it belongs:** Mounted to the robot's upper structure using the
specified screws.

**Connection:** The Raspberry Pi wiring table identifies a dedicated
connector for the WonderEcho Pro box.

## 1.10 1.9-inch display screen

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1

**What it is:** A small LCD screen.

**What it does:** Displays robot status and other visual information.
During startup, the manual describes the Hiwonder logo, language
selection, and robot status screen appearing on the LCD.

**Where it belongs:** Mounted to its LCD bracket on the robot.

**Connection:** The manual specifies a USB Type-C connection to a USB
port on the Raspberry Pi.

## 1.11 64GB microSD card

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1

**What it is:** A 64GB microSD memory card.

**What it does:** Provides storage for the robot's operating system,
software, and files.

**Where it belongs:** In the Raspberry Pi's microSD card slot.

## 1.12 Card reader

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1

**What it is:** A reader for the microSD card.

**What it does:** Lets you connect the card to a compatible computer for
reading or writing data.

**Where it belongs:** It is an accessory, not a permanently mounted
robot component.

## 1.13 Module cables and USB/Type-C cables

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1 cable group

**What the packing list specifies:** - Module cables: 150 mm and 200
mm - USB cable: 250 mm - Type-C cable: 100 mm - Type-C cable: 150 mm

**What they do:** Connect the robot's modules, computer, display, and
other electronics. Use the wiring diagrams and the connector labels to
identify each cable's destination.

**Photo notes:** Lay out the cables separately and photograph both ends
so their connectors can be identified.

## 1.14 7.4V 2200mAh battery and connection cable

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1 battery and cable

**What it is:** The robot's rechargeable 7.4V, 2200mAh battery.

**What it does:** Supplies power to the robot.

**Where it belongs:** In the battery holder on the chassis.

**Connection:** The manual specifies red to positive (+) and black to
negative (−) on the expansion board. Route the cable so it cannot
interfere with moving parts.

**Safety:** Switch the robot off while charging and use the supplied
charger. Do not short the battery terminals or modify the battery or
charger.

## 1.15 8.4V 2A charger (DC 5.5 × 2.5 mm)

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1

**What it is:** The supplied charger for the robot battery.

**What it does:** Recharges the 7.4V battery.

**Connector specified:** DC 5.5 × 2.5 mm.

**Safety:** Turn the robot off before charging. The manual says the
charger indicator is red while charging and green when charging is
complete (when connected to AC power and the battery).

## 1.16 EVA color blocks (35 mm)

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1 set

**What they are:** Colored EVA blocks, listed as 35 mm.

**What they are for:** Physical objects for robot vision, recognition,
tracking, and pick-up activities.

## 1.17 Accessory pack (screws and nuts)

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1 pack

**What it is:** A pack of mounting hardware.

**What it does:** Fastens the chassis, electronics, sensors, brackets,
and other assemblies.

## 1.18 Screwdriver and cross wrench

**Official Hiwonder reference:** [Official Ultimate Kit packing list](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-1-2-packing-list)

**Quantity in packing list:** 1 tool set

**What they are:** The hand tools supplied for assembly.

**What they do:** Help tighten and loosen the screws and nuts used on
the robot.

------------------------------------------------------------------------

# 2. LiDAR expansion pack

The Ultimate Kit includes the LiDAR components listed below. The manual
identifies the sensor as a COIN-D6 LiDAR.

## 2.1 COIN-D6 LiDAR

**Official Hiwonder reference:** [Official LiDAR assembly instructions](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-4-completing-assembly-and-wiring)

**Quantity in packing list:** 1

**What it is:** A laser distance-measuring sensor.

**What it does:** Measures distances around the robot. ClawPi uses LiDAR
for applications such as obstacle avoidance, following, mapping, and
autonomous navigation.

**Where it belongs:** Mounted on the LiDAR bracket on the upper part of
the robot.

## 2.2 LiDAR bracket

**Official Hiwonder reference:** [Official LiDAR assembly instructions](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-4-completing-assembly-and-wiring)

**Quantity in packing list:** 1

**What it is:** The mounting bracket for the LiDAR.

**What it does:** Holds the LiDAR securely in its intended position
above the robot.

**Where it belongs:** On the robot's upper structure. The manual
describes securing it with the specified screws and nylon standoffs.

## 2.3 LiDAR cable (100 mm) and Type-C cable (100 mm)

**Official Hiwonder reference:** [Official LiDAR assembly instructions](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-4-completing-assembly-and-wiring)

**Quantity in packing list:** 1 cable group

**What the packing list specifies:** - LiDAR cable: 100 mm - Type-C
cable: 100 mm

**What they do:** Provide the connections needed for the LiDAR and its
interface. Follow the wiring diagram for the correct ports.

## 2.4 LiDAR screw pack

**Official Hiwonder reference:** [Official LiDAR assembly instructions](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-4-completing-assembly-and-wiring)

**Quantity in packing list:** 1 pack

**What it is:** The dedicated screw pack listed with the LiDAR expansion
components.

**What it does:** Supplies mounting hardware for the LiDAR assembly.

**Assembly detail in the manual:** The LiDAR bracket is secured with PM4
× 8 pan-head screws and M4 × 35 + 6 single-pass nylon standoffs. The
LiDAR is secured to the bracket with PM3 × 8 pan-head screws.

------------------------------------------------------------------------

# 3. 2DOF robotic arm expansion pack

The Ultimate Kit includes a two-degree-of-freedom robotic-arm expansion
pack. The packing list names a metal gripper and a robotic arm linkage
assembly. The assembly instructions also identify a lift servo and a
gripper servo.

## 3.1 Metal gripper

**Official Hiwonder reference:** [Official robotic-arm and gripper assembly instructions](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-4-completing-assembly-and-wiring)

**Quantity in packing list:** 1

**What it is:** The metal gripping tool at the end of the robotic arm.

**What it does:** Opens and closes to hold objects, allowing the robot
to perform pick-up and grasping activities.

**Where it belongs:** At the end of the robotic arm linkage assembly.

**Servo connection:** The gripper servo is Servo No. 4 on the expansion
board.

## 3.2 Robotic arm linkage assembly

**Official Hiwonder reference:** [Official robotic-arm and gripper assembly instructions](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-4-completing-assembly-and-wiring)

**Quantity in packing list:** 1 assembly

**What it is:** The mechanical arm structure and linkages supplied for
the robot.

**What it does:** Positions and moves the gripper so the robot can reach
and pick up objects.

**Where it belongs:** Mounted to the robot chassis, with the metal
gripper attached to the end.

**Servo connection:** The arm lift servo is Servo No. 3 on the expansion
board.

## 3.3 Robotic-arm lift servo (assembly/wiring reference)

**Official Hiwonder reference:** [Official robotic-arm and gripper assembly instructions](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-4-completing-assembly-and-wiring)

**Packing-list status:** The packing list does not list this as a
separate item; it is identified in the assembly and wiring instructions
as the arm's Servo No. 3.

**What it does:** Raises and lowers the robotic arm.

**Connection:** Expansion-board servo port No. 3.

## 3.4 Gripper servo (assembly/wiring reference)

**Official Hiwonder reference:** [Official robotic-arm and gripper assembly instructions](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-4-completing-assembly-and-wiring)

**Packing-list status:** The packing list does not list this as a
separate item; it is identified in the assembly and wiring instructions
as Servo No. 4.

**What it does:** Opens and closes the metal gripper.

**Connection:** Expansion-board servo port No. 4.

------------------------------------------------------------------------

# 4. Wiring and component reference

## 4.1 Expansion-board port map

**Official reference:** [Expansion-board wiring diagram](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-5-expansion-board-wiring) · [Raspberry Pi wiring diagram](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-6-raspberry-pi-wiring) · [Product assembly photographs and steps](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html#_1-2-product-assembly)


  Port    Component/function
  ------- ------------------------------------------
  No. 1   Camera pan-tilt --- vertical tilt servo
  No. 2   Camera pan-tilt --- horizontal pan servo
  No. 3   Robotic-arm lift servo
  No. 4   Gripper servo
  No. 5   LiDAR
  No. 6   Four-channel line follower sensor
  M1      Front-left encoder motor
  M2      Rear-left encoder motor
  M3      Front-right encoder motor
  M4      Rear-right encoder motor


# 5. Safety reminders

-   Switch the robot off before changing wiring or installing
    components.
-   Do not touch conductive parts with metal objects while the robot is
    powered.
-   Never force a powered servo to move by hand.
-   Keep fingers clear of the arm, gripper, wheels, and other moving
    joints.
-   Stop operating a servo if an obstruction prevents it from moving
    freely; a stalled servo can overheat and be damaged.
-   Allow motors and servos to cool after extended operation.
-   Charge the battery with the supplied charger and keep the robot
    switched off while charging.
-   Check cable routing so wires cannot catch in wheels, linkages, or
    moving joints.
-   Follow the official assembly diagrams for screw sizes, connector
    orientation, and port locations.

------------------------------------------------------------------------

# 6. Source and scope

This inventory is based on the Ultimate Kit packing list and
assembly/wiring information in the official [Hiwonder ClawPi User
Manual](https://wiki.hiwonder.com/projects/ClawPi/en/latest/docs/1.%20ClawPi%20User%20Manual.html).

The manual's Ultimate Kit packing list identifies the Standard Kit
contents, the COIN-D6 LiDAR expansion components, and the robotic-arm
expansion components. Some items are supplied as sets or assemblies, and
the packing list does not enumerate every internal piece. The arm lift
and gripper servos are included here as **assembly/wiring references**,
not as separately confirmed loose packing-list items.

For exact quantities of small hardware, connector pinouts, and
installation orientation, consult the official manual's assembly
diagrams and the physical contents of your particular package.
