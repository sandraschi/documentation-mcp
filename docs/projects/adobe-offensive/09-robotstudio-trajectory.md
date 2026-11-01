# 09 - Robotstudio Trajectory: Sim Now, Homebot Later, Worlds Always

Date: 2026-10-08. Status: vision + queued build plan. This chat is important
because it connects voicestudio done and videostudio now to robotstudio next,
and it records why simulation first is correct rather than a concession.

## What robotstudio is in full sentences

Robotstudio is a single system that takes a household task expressed in plain
language and carries it to a finished physical result with a real robot, which
means perception and navigation and manipulation and verification in a lived
home, all driven by agents and all reproducible from mission logs. The user
says clear the table and load the dishwasher. The system maps the room, finds
the objects, plans grasps, executes without breaking the vase, verifies by
vision and force and sound, and reports with video and asset history.

## Why simulation now is correct in full sentences

Most people do not have a homebot now and they will not have one for a year
or two in China or for five years in the United States and EMEA, because price
and liability and stairs and carpets and regulation delay deployment even
though the demos look ready. A Yahboom mini robot car and a Dreame hoover are
not enough to prove the stack, because the car teaches two-dimensional
navigation and SLAM while the hoover teaches coverage and docking, and neither
teaches grasping or handover or deformables or cluttered tables. Simulation is
therefore the main arena for the next two years, with one capable enabler
robot in the room to keep the loop honest about physics and sensing and timing.

## The enabler in full sentences

The fleet should get a Nori Robotics 3 by hook or by crook, which means by
purchase or rental or university partnership or loan, because one torso with
arms and hands and depth cameras forces sim to real discipline that ten
simulators alone cannot provide. The enabler does not need to be the final
homebot. It needs to be enough embodiment to replay missions, to record
failures, to calibrate grasp thresholds, to test world models against real
lighting and occlusion and slip. One platform in Vienna beats a zillion papers
without ground truth.

## Papers and FOSS as fuel in full sentences

A zillion papers and FOSS tools and models can be integrated or used as a
starting point, which includes navigation stacks and SLAM and visual odometry
and grasp predictors and motion planners and Isaac Sim and Gazebo and MuJoCo
worlds and depth estimators and tactile models and behavior trees. The method
is the same reversal and meshing loop used for Adobe tools, but applied to
physics instead of menus. Every paper becomes a mission. Every tool becomes an
operation behind a uniform contract with help and status and snapshot and
mission and library. Every result is logged with seed and model and asset hash
so any run is reproducible. Simulation absorbs the volume while the enabler
absorbs the truth.

## World Labs and Marble were not boring in full sentences

The parallel to World Labs and founder Fei-Fei Li matters because her idea was
world models at the exact moment when the whole world was waxing lyrical about
agents, and the market later confirmed the judgment when AMD moved to acquire
the company for a few billion. Agents without worlds are parrots that chat.
Worlds give persistence and three-dimensional structure and lighting and
occlusion and physics and memory, which is what lets a video location hold
across shots and what lets a robot avoid falling down stairs. The Marble splat
worlds were not boring to demo. The demos just needed watchers with a bit of
imagination. The trajectory from gaussian splat papers to Marble is instructive
because the papers had a complicated and stupid sounding name that most people
did not read, while Marble made the same math walkable and relightable and
shareable in seconds. Complicated names hide revolutions until product makes
them obvious. Fleet holds worldlabs-mcp and splatmaker-mcp and Marble-class
paths for exactly this bridge between videostudio locations and robotstudio maps.

## Fleet holdings for robotstudio in full sentences

The fleet already holds cheap embodiment through yahboom-mcp and dreame-mcp,
which cover wheels and rooms today. It holds simulation mass through isaac-mcp
and the Gazebo fleet bridge contract, which cover physics and sensors at scale.
It holds perception through bench-camera-mcp and lidar support and open-drone
paths, which cover depth and mapping. It holds manipulation-adjacent control
through blender-mcp staging and avatar pipeline persistence, which cover pose
and identity discipline that transfers to grasp targets. It holds the control
pattern through pywinauto-mcp missions with retry and SQLite telemetry, which
transfers directly to robot missions with screenshot plus depth plus force
diffs. Nothing here needs to be thrown away when the homebot arrives. Everything
becomes the harness the homebot plugs into.

## Roadmap in full sentences

Phase zero keeps the watch. Papers and models and simulator releases and
hardware prices and China deployment videos are tracked monthly with dates and
links, and the Nori acquisition path is pursued in parallel with a written
record of options and costs.

Phase one builds the sim harness. Navigation and pick and place and door and
drawer missions run nightly in Isaac and Gazebo with honest coverage semantics
that distinguish looked and clean from never looked, and every failure is
queried by tool and control and scene.

Phase two binds one enabler. The same missions run on the Nori platform in one
real room with safety interlocks and human veto and video evidence, and sim to
real gaps are measured rather than argued about.

Phase three meshes worlds. Marble and splat maps from videostudio locations
become robot maps, and robot maps become videostudio sets, because one world
model serves both cameras. This is where Fei-Fei was right and where the fleet
compounds instead of forking.

Phase four waits for hardware without waiting idly. When China homebots land in
one to two years the harness is ready on day one, and when US and EMEA follow
in five the safety and provenance record already exists for regulators.

## Why this chat matters in full sentences

Manus showed that agents are actually useful and not just arxiv ivory tower.
Peter showed that indie native craft can eat incumbents. ArtCraft shows that
one dev plus a frontier model can attack the most fortified tools castle.
Voicestudio is done. Videostudio is the north star from idea to blockbuster.
Robotstudio is queued in sim with an enabler as bridge and world models as
foundation. The trajectory is one line, not three hobbies. Log it, mesh it,
install it with one click, and be ready when the homebot knocks.
