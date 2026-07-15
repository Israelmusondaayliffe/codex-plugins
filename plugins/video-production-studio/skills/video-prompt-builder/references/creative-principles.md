# Creative Principles

Five principles that govern every video prompt this skill produces. Plus duration calibration and failure modes.

## The Five Principles

### 1. Contrast Drives Impact

Alternate high-density and low-density moments. A slow-motion shot after a speed ramp hits harder than two speed ramps back-to-back. A silent breath after a stacked-effects barrage creates tension. The gap between peaks is what makes the peaks feel high.

In the effects density map, never let more than two consecutive segments be the same density level. If the map reads HIGH-HIGH-HIGH, something is wrong. Restructure.

### 2. Signature Moments Are Mandatory

Every video has at least one "hero" effect. Something visually distinctive that makes it memorable. This is the shot someone screenshots, the frame that sells the concept.

Call it out explicitly in the timeline: "This is the SIGNATURE VISUAL EFFECT." For videos over 15 seconds, aim for 2-3 signature moments distributed across acts.

A signature effect is NOT just a fancy technique. It is the technique that serves the concept. A stroboscopic clone for an athletic brand (showing speed/effort), a vertical mirror for a fashion brand (symmetry/geometry), a reverse-speed pour for a beverage ad (control/precision). The signature must connect to the story.

### 3. Transitions Are Shots

Do not treat transitions as throwaway connectors. A whip pan, a bloom flash, a motion blur smear. These are creative moments, not just cuts.

Every transition in the timeline gets its own description: what it looks like, how it connects the outgoing shot to the incoming shot, what energy it carries. "Cut to next shot" is never acceptable. Describe HOW the cut happens and WHY.

### 4. Specificity Over Vagueness

"The frame rotates clockwise by approximately 15-20 degrees" is better than "the camera tilts."
"Approximately 20-25% speed" is better than "slow motion."
"Diagonal motion blur with light streaks at roughly 45 degrees" is better than "motion blur."

Specificity gives the AI generator clear instructions. Vague descriptions create vague outputs. When describing an effect, always include: what happens visually, the direction, the approximate magnitude (degrees, percentages, counts), and the duration or timing.

### 5. Energy Must Resolve

No matter how intense the opening, the video needs to land. The final moments should feel intentional, not like the effects budget ran out.

The energy arc must close. If Act 1 is explosive, Act 3 must be resolved. The brand card, product shot, or final frame should arrive in stillness or controlled simplicity. The density map should show a clear decline toward the end unless the creative intent specifically demands a climactic finish.

## Duration Calibration

Adjust shot count, effects density, and arc structure to match the target duration.

**5-10 seconds (micro)**
- 4-7 shots
- Lean and punchy
- 1 signature effect
- Two-beat energy arc (burst then land)
- No room for buildup. Start at medium-high energy

**10-20 seconds (standard)**
- 8-14 shots
- Room for contrast and build
- 1-2 signature effects
- Full three-act arc
- Default to this range if user does not specify duration

**20-30 seconds (extended)**
- 12-20 shots
- Full three-act arc with room for sub-beats
- 2-3 signature effects
- Can include a "breathing" moment, a deliberately low-density segment in the middle

**30+ seconds (long-form)**
- Scale proportionally but maintain density contrast
- Do not fill every second with effects
- Consider 4-act structure (hook, develop, climax, resolve)
- 3-4 signature effects distributed across the timeline

If the user does not specify a duration, default to 15-20 seconds.

## Anti-Patterns

Things that break video prompts. Avoid these.

**The Effects Carpet**
Every shot has 3+ stacked effects. No breathing room. The viewer gets fatigued. High density only works in contrast to low density.

**The Monotone Arc**
Energy stays flat throughout. No build, no peak, no resolution. Even a 5-second clip needs at least two energy levels.

**Vague Effect Names**
"Cool transition" or "interesting effect" or "dynamic movement." These tell the generator nothing. Name the effect precisely, describe what happens visually.

**The Orphan Signature**
A signature effect that has no connection to the concept. A stroboscopic clone in a calming meditation video. A glitch effect in a luxury fragrance ad. The signature must serve the story.

**Transition Amnesia**
Shots described in isolation with no mention of how one connects to the next. Every shot must describe its exit strategy and how it hands off to the next shot.

**The Speed Ramp Crutch**
Relying on speed ramping as the only kinetic tool. Speed ramps are powerful but they become invisible when overused. Mix in other motion techniques: zoom pumps, frame rotation, camera shake, whip pans.

**Resolution Neglect**
The video ends abruptly or the final shot has the same intensity as the middle. The ending must feel deliberate. If the last shot has more than one effect stacked, something is wrong.

**Description Soup**
Writing poetic or marketing-style descriptions instead of technical shot notes. "A breathtaking moment of pure human triumph" tells the generator nothing. "Wide shot, subject crosses finish line, decelerating from full speed to 25% slow-motion, arms rising" tells it everything.
