# CLAUDE.md

## The plan
Team Picker builds a robot (Hiwonder ClawPi) that picks up cubes in a room and brings them to the drop zone. Team Scout finds the cubes, we fetch them. Every change should move us toward that goal. If a task doesn't fit it, ask first.

## Ask, don't guess
If a requirement, design choice or acceptance criterion is unclear, ask the user before building. Several small questions are better than a wrong implementation.

## Work from the issue
- We work in the GitHub organisation `SRH-AI-AUTOMATION-GARBAGE-PICKERS`. Work items are issues on the project board.
- The user gives you the issue number. Read it with `gh issue view <n>` and follow its tasks, acceptance criteria and Definition of Done ([docs/definition-of-done.md](docs/definition-of-done.md)).
- Reference the issue in commits and in the PR (`Closes #<n>`).

## Branches and pull requests: main stays clean
- Never commit or push to `main`. Every change goes on its own branch and into `main` only through a pull request.
- Branch name: `<issue>-<short-name>`, e.g. `16-stop-command`.
- Commit message: `<type>: <what changed> (#issue)`, where type is `feat`, `fix`, `docs`, `test` or `chore`.
- One issue = one branch = one PR. Keep PRs small.
- A teammate who didn't write the PR approves it. Don't merge PRs yourself.
- The only exception is the Scrum Master's lab protocol (`Protocols/SN.md`), which may go directly to `main`.
- Full rules are in the wiki page "Workflow".

## Documentation goes in the wiki
- Docs, test results and how-tos go in the GitHub wiki, not in new files in this repo: https://github.com/SRH-AI-AUTOMATION-GARBAGE-PICKERS/The-garbage-picker/wiki
- The wiki is a separate git repo: `https://github.com/SRH-AI-AUTOMATION-GARBAGE-PICKERS/The-garbage-picker.wiki.git`. Pushes there go live immediately with no PR, so confirm the content with the user before pushing.
- Code-level READMEs (like `src/picker_sim/README.md`) stay with the code. Link them to the wiki instead of copying text.

## Robot and simulation
- ROS 2 Humble + Gazebo Fortress, package `src/picker_sim`. Setup and usage: [src/picker_sim/README.md](src/picker_sim/README.md).
- On Ubuntu 24.04 the sim runs in the Docker container `humble`, with this repo mounted at `/root/ros2_ws/src/The-garbage-picker`.
- Safety requirements (speed limits, stop rules): [docs/picker-safety-requirements.md](docs/picker-safety-requirements.md). New motion code runs in the sim first (SR-23).
