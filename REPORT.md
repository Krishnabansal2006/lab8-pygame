# Project Report: AI-Assisted Development

## 1. Initial Approach

**Understanding:** I started with 10 basic moving squares and added features
one at a time — increasing to 20 squares, size-based speed, jitter, flee
behavior, wall steering, life span, and particle rebirth.

**Assumptions:** I assumed the flee feature would be simple but it involved
vectors, distances, and blending which took time to understand and get right.

**Points needing clarification:** I was not sure at first whether to use
vector rotation or vector addition for the flee force. I ended up using
vector addition with distance weighting.

## 2. Prompting and AI Interaction

**Successes:** Asking Copilot to explain concepts like atan2, vector
normalization, and distance weighting worked well. It explained without
writing the code for me which helped me actually understand.

**Failures:** When I asked for the full code it gave me everything at once
and I lost track of what was happening. Indentation errors also happened
because I was copy pasting instead of writing myself.

**Analysis:** The failures happened when I relied too much on getting
complete solutions. Understanding each piece separately worked much better.

## 3. Key Learnings

**Technical Skills:** I learned how vector math works in practice — using
math.hypot for distance, math.atan2 for angle, and cos/sin to rebuild a
velocity vector from angle and speed. I also learned how dt makes movement
frame-rate independent and why that matters.

**New concepts:** Particle systems, pending spawn timers, time-based
animation, soft wall steering, and blending velocity vectors.

**AI Workflow:** Copilot is most useful for explaining concepts and reviewing
code. Writing code myself then asking for review works better than asking
for the full solution. When I copy pasted without understanding, I introduced
bugs I could not fix because I did not know what the code was doing.

**Would I use AI the same way next time:** I would use Ask Mode more and
Agent Mode less for the core logic. For boilerplate and documentation,
Agent Mode saves a lot of time.