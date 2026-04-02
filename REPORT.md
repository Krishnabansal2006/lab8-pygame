# Project Report: AI-Assisted Development

## 1. Initial Approach
**Understanding:** I started by getting the basic 10 squares working from last week,
then added features one at a time - increasing to 100 squares, adding size-based
speed limits, and finally the jitter effect.

**Assumptions:** I assumed the jitter would be simple to add but it turned out the
direction timer and jitter were fighting each other, so I had to remove the old
direction system completely.

## 2. Prompting & AI Interaction
**Successes:** Asking Copilot to explain concepts like atan2 and vector rotation
worked well. It gave clear answers without writing the code for me.

**Failures:** When I asked for the full code directly it gave me everything at once
and I lost track of what each part was doing. I also had indentation errors because
I was copy pasting instead of writing myself.

**Analysis:** The failures happened when I relied too much on copy paste. When I
typed the code myself I understood it better and caught errors faster.

## 3. Key Learnings
**Technical Skills:** I learned how vector rotation works using atan2, cos and sin.
I also learned that math.hypot gives you the magnitude of a vector, and that
rotating a vector preserves its speed.

**AI Workflow:** Next time I will write more code myself and only use Copilot to
review or explain. Copy pasting full functions without understanding them causes
more problems than it saves time.