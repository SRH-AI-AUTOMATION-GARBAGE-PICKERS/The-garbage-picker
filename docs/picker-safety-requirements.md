# Picker Robot: General Safety Requirements and Proposed Limits

| | |
|---|---|
| **Robot** | Hiwonder ClawPi Ultimate Kit: Raspberry Pi 5, 4× Mecanum drive, arm + metal gripper, COIN-D6 LiDAR, 7.4 V 2200 mAh battery [27] |
| **Course** | AI and Autonomous Systems Lab, SRH Leipzig |
| **Author** | Developer / Safety Specialist |
| **Version** | 0.1 draft, 2026-11-17, for team review |

## Aim

This document gives the safety requirements and the operation limits for the Picker robot. The purpose is to prevent injury to persons and damage to the room and to the robot. The document gives the applicable regulations, the limits for speed, distance, force and battery operation, and a checklist to examine each limit. The university must do a risk assessment for the robot (BetrSichV §3). This document gives the data from our team for that risk assessment.

The robot can cause four dangers. The base and the arm can hit persons and objects. The gripper can catch the fingers of a person. A malfunction of the software or the network can cause movement that the operator does not expect. The lithium battery or a hot servo can cause a fire or burn a person.

The robot also has these problems. The manufacturer installed no safety devices on the robot. The 2D LiDAR cannot find table edges or low objects. The manufacturer does not give the maximum arm speed or the maximum payload. The robot gets all control signals through Wi-Fi. The control hardware has no safety rating.

These are the most important limits:

- The maximum speed of the arm is 250 mm/s.
- The maximum speed of the base is 0.3 m/s.
- When a person is less than 1.0 m from the robot, the maximum speed of the base is 0.1 m/s.
- When a person or an object is less than 0.4 m from the robot, the robot stops.
- The maximum force of the gripper is 25 N.
- When the robot gets no control signal for 500 ms, the robot stops.
- The minimum voltage of the battery is 6.6 V.

The limit for the arm speed comes from ISO 10218-2:2025. Our team selected the other limits.

Requirement tags: **[LAW]** = binding legal obligation, **[STD]** = value or practice taken from a standard, **[PROP]** = our own proposed limit (engineering judgement, not from a standard).

---

## 1. Applicable regulations and standards

### 1.1 Binding law

| Regulation | Applies to us? | What it requires / why it matters |
|---|---|---|
| **ArbSchG §5 + BetrSichV §3** (DE) | **Yes** (university as employer) | Hazards must be assessed and protective measures derived *before* any work equipment is used [22]. The result must be documented before first use [22]. Students who use work equipment count as employees for this purpose [23]. A CE mark does not remove the duty to do a risk assessment [22]. **This document is our input to that assessment.** |
| **DGUV Vorschrift 1** + SGB VII §2(1) Nr. 8c | **Yes** | Students at universities are insured persons, so accident prevention regulations apply to them [24]. Sector guidance: DGUV Regel 102-603 "Branche Hochschule" [26]. |
| **DGUV Vorschrift 3 / 4** (electrical) | **Yes**, for mains equipment (charger, PSUs) | Which one applies depends on the accident insurer: V3 for commercial Berufsgenossenschaften, V4 for public-sector insurers. Students are insured persons either way [25]. |
| **Machinery Directive 2006/42/EC → Machinery Regulation (EU) 2023/1230** | **Reference only** | Most of the Regulation applies from 20 Jan 2027. Machinery placed on the market before then must comply with the 2006 Directive [16]. It explicitly targets autonomous mobile machinery and AI [16]. We don't sell anything, but an in-house build *could* count as "putting into service". **Confirm with the university's Fachkraft für Arbeitssicherheit.** |
| **General Product Safety Regulation (EU) 2023/988** | No (we don't sell) | Has applied since 13 Dec 2024 as a safety net for non-food products not covered by specific laws [17]. It is the kit vendor's obligation. |
| **Low Voltage Directive 2014/35/EU** | Robot: **no**. Charger: **yes** | Covers 50–1000 V AC and 75–1500 V DC [18], so the 7.4 V robot is outside its scope. Battery equipment that runs from a mains PSU can be inside the scope [18]: **use only the CE-marked charger supplied with the kit.** |
| **Radio Equipment Directive 2014/53/EU** | Kit vendor; relevant to us if we modify | The Pi 5's Wi-Fi falls under RED. Its cybersecurity delegated act (EU) 2022/30 has applied since Aug 2025 and is repealed by (EU) 2026/339 [19], with effect from 11 Dec 2027 [19]. **Do not modify radio hardware or antennas.** |
| **Batteries Regulation (EU) 2023/1542** | **Yes**, for disposal | Has applied since 18 Feb 2024 [20]. Uncollected Li-ion batteries are a fire hazard in waste streams [20]. **Dispose of batteries only at a battery collection point.** |
| **AI Act (EU) 2024/1689** | Not applicable | Article 2 excludes pure scientific R&D and pre-market testing and development [21]. Our perception and planning stack is never placed on the market. |

### 1.2 Standards (voluntary, define "state of the art")

None of these is formally mandatory for a 7.4 V educational kit. We use them for method and numbers.

| Standard | Status (Nov 2026) | What we take from it |
|---|---|---|
| **ISO 12100** | Current | Risk assessment and risk reduction method, used in the EU [11] |
| **ISO 13849-1:2023** | Current. EN 2015 edition withdrawn after 15 May 2027 [11] | Required Performance Level (PLr), PL a (low) to PL e (high) [11] |
| **ISO 10218-1:2025 / -2:2025** | Published Feb 2025 [2]. Harmonised in EU OJ 7 Sep 2026 [2] | Robot classes, mandatory safety functions, reduced speed, contact limits (see §3). Scope excludes consumer products [1] |
| **ISO/TS 15066:2016** | Superseded in practice: most content moved into ISO 10218-2:2025 [3] | Body-region force limits, now in ISO 10218-2:2025 Annex M [6] |
| **ISO 13482** | 2014 edition current. Revision at FDIS ballot since 17 Sep 2026 [8] | Closest scope match: service robot in a shared, non-industrial space |
| **ISO 3691-4:2023** | Current [9] | Driverless trucks/AMRs. Excludes robots for public zones and points those to ISO 13482 [9] |
| **ANSI/A3 R15.08-1/-2/-3** | Parts 1–3 republished as a set Apr 2026 [10] | "IMR Type C" = mobile platform with a manipulator attached [10], which is exactly the Picker |
| **ISO 13850:2015** | Current [12] | E-stop design principles. Electrical implementation is per IEC 60204-1 [12] |
| **IEC 60204-1:2016+AMD1:2021** | Current [13] | Electrical equipment of machines, including e-stop and stop categories [13] |
| **IEC 62133-2:2017+AMD1:2021** | Current [14] | Safety of portable Li cells and batteries: overcharge, short circuit, drop, crush tests [14] |
| **IEC 60825-1:2014** | Current [15] | Laser safety. The COIN-D6 (905 nm) is listed as IEC 60825-1 certified [15]; class not stated in the listing |

---

## 2. Hazard overview

| # | Hazard | Source | Possible harm |
|---|---|---|---|
| H1 | Impact / collision | Moving base, swinging arm | Bruising, finger/hand injury, tripping |
| H2 | Pinching / clamping | Gripper jaws, arm links | Finger pinch |
| H3 | Unexpected start-up | Software bug, stale command, network intruder | Any of H1/H2 |
| H4 | Fire / thermal | Li battery (overcharge, short, puncture), stalled servo | Burns, fire |
| H5 | Fall from height | Robot driving off a table | Robot damage, damage to objects below, foot injury |
| H6 | Damage to environment | Collision, dropped payload | Damaged furniture/equipment |
| H7 | Damage to robot | Joint over-travel, self-collision, servo stall, deep discharge | Broken servos/links, dead battery |
| H8 | Laser radiation | LiDAR | Eye exposure (low risk if Class 1, see O3) |

---

## 3. Requirements

### 3.1 People

| ID | Requirement | Tag |
|---|---|---|
| SR-01 | A **hardware emergency stop** shall be fitted: a latching red mushroom switch on a yellow background that directly cuts power to motors and servos (Pi stays powered). Resetting it shall not restart motion by itself. | [STD] ISO 13850 [12], IEC 60204-1 [13] |
| SR-02 | The e-stop function shall reach at least **PL c**. Protective stop and reduced speed shall reach at least **PL d** (ISO 10218-2:2025 default values). A ROS node publishing zero velocity is a *protective stop*, not an e-stop. | [STD] [2] |
| SR-03 | A **command watchdog** shall stop all motion if no valid `cmd_vel` / arm command arrives for **500 ms** (covers Wi-Fi loss and crashed nodes). | [PROP] |
| SR-04 | **Arm TCP speed ≤ 250 mm/s** at all times while people are in the lab. This matches the ISO 10218 reduced-speed limit [2] and the Class I speed threshold [4]. | [STD] |
| SR-05 | **Base speed ≤ 0.3 m/s** linear, **≤ 1.0 rad/s** angular. | [PROP] |
| SR-06 | **Separation zones** from the robot outline, using the LiDAR: slowdown to **0.1 m/s inside 1.0 m**, stop **inside 0.4 m**. Implementation: Nav2 Collision Monitor (stop / slowdown polygons; the most restrictive zone wins) [28]. | [PROP], SSM principle [3] |
| SR-07 | **Gripper pinch force ≤ 25 N** (servo torque capped, measured with a force gauge or kitchen scale). That is far below the 140 N quasi-static hand/finger limit [6] and also protects payloads. | [PROP], [STD] reference |
| SR-08 | **One designated operator** holds or stands within reach of the e-stop during every powered run. No hands inside the arm's reach while actuators are powered. | [PROP] |
| SR-09 | A **visible indicator** (LED or screen) shows when actuators are powered or enabled. | [PROP] |

### 3.2 Environment

| ID | Requirement | Tag |
|---|---|---|
| SR-10 | Operate **on the floor** in a marked test area. No table-top driving unless edges are blocked or cliff sensors are fitted. The 2D LiDAR does not see table edges or objects below its scan plane. | [PROP] |
| SR-11 | Clear the test area of cables, bags and fragile items before each run. | [PROP] |
| SR-12 | **Payloads:** only objects the team has tested. Start with **≤ 50 g**, non-fragile (foam, plastic). Increase only after a documented test. | [PROP] |
| SR-13 | Base **stopping distance from 0.3 m/s ≤ 0.15 m** (measured), so the robot stops before the 0.4 m stop zone is crossed. | [PROP] |

### 3.3 Robot itself

| ID | Requirement | Tag |
|---|---|---|
| SR-20 | **Software joint limits 5° inside the mechanical stops.** Self-collision check against the chassis and LiDAR mast before executing any arm trajectory. | [PROP] |
| SR-21 | **Stall detection:** if a servo's position error persists **> 1 s**, cut torque on that servo and raise an error. | [PROP] |
| SR-22 | **Battery** (if Li-based 2S, see O2): cut-off at **6.6 V** under load (3.3 V/cell), storage at **7.6 V** (3.8 V/cell), charge at **≤ 1C (2.2 A)**, supervised, in a LiPo bag. Never leave charging unattended. Remove from service if swollen or damaged. | [PROP], IEC 62133-2 context [14] |
| SR-23 | New motion code runs first in **simulation or at 50 % of the limits above**, with the robot lifted or on blocks, before running on the floor. | [PROP] |

### 3.4 Network / cybersecurity

Unauthorised commands are a safety hazard (H3). ISO 10218:2025 adds safety-related cybersecurity requirements [3].

| ID | Requirement | Tag |
|---|---|---|
| SR-30 | The robot connects only to an **isolated, WPA2/WPA3-protected access point**. No open lab or eduroam networks. | [PROP] |
| SR-31 | Use a **unique `ROS_DOMAIN_ID`** per team (Scout ≠ Picker) so one robot cannot receive the other's topics. | [PROP] |
| SR-32 | **Change the default passwords** on the Pi image and app connection before first use. | [PROP] |

---

## 4. Proposed limits (summary)

| Parameter | Limit | Basis |
|---|---|---|
| Arm TCP speed | ≤ 250 mm/s | ISO 10218-2:2025 reduced speed [2] |
| Base linear speed | ≤ 0.3 m/s | Proposal |
| Base speed, person within 1.0 m | ≤ 0.1 m/s | Proposal |
| Base angular speed | ≤ 1.0 rad/s | Proposal |
| LiDAR stop zone | 0.4 m from outline | Proposal |
| Stopping distance from 0.3 m/s | ≤ 0.15 m | Proposal |
| Command watchdog | 500 ms | Proposal |
| Gripper pinch force | ≤ 25 N | Proposal (ISO limit 140 N [6]) |
| Initial payload | ≤ 50 g | Proposal |
| Joint soft-limit margin | 5° | Proposal |
| Servo stall timeout | 1 s | Proposal |
| Battery cut-off / storage (2S Li) | 6.6 V / 7.6 V | Proposal |
| Charge current | ≤ 2.2 A (1C) | Proposal |
| E-stop / protective stop PL | PL c / PL d | ISO 10218-2:2025 defaults [2] |

**Reference values from ISO 10218-1/-2:2025 (formerly ISO/TS 15066):**
- Robot Class I: manipulator mass ≤ 10 kg, force ≤ 50 N, TCP speed ≤ 250 mm/s, judged by the arm's raw capability, not by limits set in software [5]. Class I has much lower requirements [4].
- Quasi-static contact force limits: skull 130 N, face 65 N, chest 140 N, hands/fingers 140 N, lower arm 160 N, thighs/knees 220 N. Transient contact may be up to 2× higher [7].

---

## 5. Verification checklist

| Check | When | Method | Pass |
|---|---|---|---|
| V1 E-stop | Before every session | Command motion, press e-stop | All actuators stop. No restart on reset |
| V2 Watchdog | After any comms code change | Kill teleop node / disconnect Wi-Fi during motion | Stops within 500 ms |
| V3 Arm speed | Once, plus after arm config changes | Film at full servo speed next to a ruler, compute TCP speed | ≤ 250 mm/s with limits on. Record raw max for O1 |
| V4 Stopping distance | Once, plus after tuning | Drive at 0.3 m/s, trigger stop, measure | ≤ 0.15 m |
| V5 Zones | After Nav2 config changes | Walk towards the robot | Slows at 1.0 m, stops at 0.4 m |
| V6 Gripper force | Once | Close the gripper on a force gauge or scale | ≤ 25 N |
| V7 Battery | Weekly | Visual check for swelling and damage, voltage | No swelling. Stored at about 7.6 V |

---

## 6. Open items

| # | Item | Owner | Action |
|---|---|---|---|
| O1 | Arm's raw maximum TCP speed (decides Class I vs II) | Safety | V3 test |
| O2 | Battery chemistry (LiPo / Li-ion / NiMH) | Safety | Read the battery label. SR-22 values assume 2S Li |
| O3 | LiDAR laser class | Safety | Read the COIN-D6 label (expected Class 1) |
| O4 | Does the university treat the build as machinery being put into service? | Safety + lecturer | Ask the Fachkraft für Arbeitssicherheit |
| O5 | Integration into the university's Gefährdungsbeurteilung (BetrSichV §3) | Lecturer | Hand over this document |

---

## Sources

1. ISO 10218-1:2025 scope and life cycle: https://genorma.com/en/standards/iso-10218-1-2025
2. ibf solutions, "The new standards for industrial robots: EN ISO 10218-1 and -2" (safety function table, default PLr, reduced speed, EU OJ listing): https://www.ibf-solutions.com/en/seminars-and-news/news/new-standards-for-industrial-robots-en-iso-10218-1-and-2
3. There's a Robot for That, "ISO 10218:2025 explained": https://theresarobotforthat.com/blog/iso-10218-2025-explained/
4. KAN Brief 2/23, "Revision of EN ISO 10218": https://www.kan.de/en/publications/kanbrief/2023/2-23/revision-of-en-iso-10218-safety-requirements-for-industrial-robots/
5. Ferraro, Freda, Pera (INAIL), "New Standards for Industrial Robots", ESREL 2025: https://rpsonline.com.sg/proceedings/esrel-sra-e2025/pdf/ESREL-SRA-E2025-P3635.pdf
6. Robotiq, "Compliance of the Hand-E gripper with ISO 10218-2:2025" (Annex M, 140 N): https://blog.robotiq.com/knowledge/compliance-of-the-hand-e-gripper-with-iso-10218-22025
7. Webiano, "ISO/TS 15066" body model and limits: https://webiano.digital/knowledge-base/robotics/robot-safety/iso-ts-15066/
8. FprEN ISO 13482 (ISO/FDIS 13482:2026) status: https://genorma.com/en/standards/fpren-iso-13482
9. ISO 3691-4 scope (2020 edition superseded by 2023): https://shop.standards.ie/en-ie/standards/iso-3691-4-2020-1182044_saig_iso_iso_2821155
10. A3 Store, ANSI/A3 R15.08 Parts 1–3: https://www.automate.org/store/products/ansi-a3-r15-08-american-national-standard-for-industrial-mobile-robots-imrs-imr-systems-and-imr-applications-safety-requirements-parts-1-2-and-3-pdf-download and ANSI blog (IMR Type C): https://blog.ansi.org/?p=190951
11. Pilz, EN ISO 13849-1 (PL, 2023 edition, transition to 15 May 2027, ISO 12100): https://www.pilz.com/en-ES/support/law-standards-norms/functional-safety/en-iso-13849-1/index.html
12. DIN EN ISO 13850:2016-05 (ISO 13850:2015): https://www.din.de/en/wdc-beuth:din21:233572513
13. IEC 60204-1:2016 (+AMD1:2021): https://online.standard.no/en/iec-60204-1-2016-ed6
14. IEC 62133-2:2017+AMD1:2021 overview: https://www.batterydesign.net/legislation-rules-and-regulations/iec-62133-2/
15. IEC 60825-1:2014: https://www.iecee.org/certification/iec-standards/iec-60825-12014 and COIN-D6 specs: https://rcdrone.top/products/witmotion-dtof-lidar
16. Baker McKenzie, Machinery Regulation 2023/1230: https://www.bakermckenzie.com/en/insight/publications/resources/product-risk-radar-articles/machinery-regulation
17. EU-OSHA, Regulation 2023/988 (GPSR): https://osha.europa.eu/de/legislation/directive/regulation-2023988eu-general-product-safety
18. Element, EC guide to the Low Voltage Directive: https://www.element.com/resources/articles/the-european-commissions-guide-to-the-low-voltage-directive
19. European Commission, Radio Equipment Directive: https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/radio-equipment-directive-red_en and repeal of 2022/30 (C(2026) 778): https://data.consilium.europa.eu/doc/document/ST-6429-2026-INIT/en/pdf
20. European Commission, Batteries Regulation 2023/1542: https://environment.ec.europa.eu/waste/batteries/legislation.htm
21. AI Act Article 2 (scope and exclusions): https://www.springlex.eu/en/packages/ai-act/ai-act-regulation/article-2/
22. BetrSichV §3: https://www.gesetze-im-internet.de/betrsichv_2015/__3.html
23. BetrSichV §2 (students equal to employees), text edition: https://www.forum-verlag.com/media/pdf/LP_3088_BetrSichV.pdf
24. KomNet Dialog 42628, DGUV Vorschrift 1 for students: https://www.komnet.nrw.de/_sitetools/dialog/42628
25. KomNet Dialog 23721, DGUV Vorschrift 3/4 at universities: https://www.komnet.nrw.de/_sitetools/dialog/23721
26. DGUV Regel 102-603 "Branche Hochschule": https://publikationen.dguv.de/widgets/pdf/download/article/4346
27. OpenELAB, Hiwonder ClawPi ROS2 kit: https://openelab.io/a/s/products/hiwonder-clawpi-ros2-robot
28. Nav2 Collision Monitor configuration: https://docs.nav2.org/configuration/packages/collision_monitor/configuring-collision-monitor-node.html
