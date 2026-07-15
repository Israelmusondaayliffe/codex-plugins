# Adapted Miessler Prompt Library

Source: Daniel Miessler, "10 Prompts to Run Before Fable Goes Away" (June 2026), adapted
for a Cowork or Claude Code harness. Em-dashes removed per house style. Each prompt
runs at the highest effort tier available (xhigh on the Claude 5 family). Read only the section for the audit being executed.

## Contents
- HARNESS: goal-orientation, bitter-lesson, self-model, memory-compounding, define-better, autonomy-ladder
- SECURITY: prompt-injection, attack-surface
- LIFE: big-picture, most-wrong, 10x-or-dies, decisions-into-policy, binding-constraint, bus-factor
- APPENDIX: maintenance loop, blog consolidation

---

## HARNESS

### goal-orientation

```
Look at our overall harness and characterize what I am ultimately trying to accomplish
with it. Then find the parts of the system, the system prompt, CLAUDE.md and context
files, hooks, skills, and the rest, that are working against that goal. And if you do
not see a clear goal in the harness at all, interview me about it so we can get the
whole system pulling in a single direction.
```

### bitter-lesson

```
Deeply study Richard Sutton's Bitter Lesson essay and how it applies to overengineering,
specifically for AI and coding harnesses. Then do a full analysis of our harness in its
entirety, look for every place we are violating Bitter Lesson engineering, and give me a
comprehensive plan for upgrading the system to be more flexible to future improvements
in the models we use.
```

### self-model

```
Read everything my harness believes about me: identity, goals, voice, preferences. Find
where it is modeling a version of me that is stale, aspirational, or just wrong. Compare
what my files say I am against what my recent behavior and work actually reveal, flag
every place the system is optimizing for who I said I was instead of who I am now, and
propose the specific edits that close the gap.
```

### memory-compounding

```
Look at everything my harness remembers and how it learns across sessions. Find where
knowledge goes to die, captured but never resurfaced, or never captured at all. Tell me
whether it is actually getting smarter about me or just accumulating. Then design the
retention, decay, and promotion rules that make every session compound into the next.
```

### define-better

```
I cannot improve what I cannot measure. Define what better actually means for my harness,
not vanity metrics, the thing I really care about. Build the evals and regression checks
that catch it getting worse before I feel it. And find where I am already optimizing a
proxy that is quietly drifting from what I actually want.
```

### autonomy-ladder

```
Map what my harness does on its own versus what it asks me to approve. Find where I have
handed an agent authority it should not have, and where I am withholding authority out
of fear and paying for it. Calibrate each action by risk against leverage, not habit.
Then redesign the trust boundary so it is neither reckless nor asking permission for
everything.
```

---

## SECURITY

### prompt-injection

```
Do a deep analysis of our overall harness and model how vulnerable it is to various
levels of prompt injection. Map out all the different inputs to the harness, and how
each input avenue is handled from a prompt-injection standpoint and with which models.
Based on the data and tools we have access to, figure out what our prompt-injection
defense should be, research the best tools available, and give me a full plan and
recommendation for upgrading the harness over the long term so it is less vulnerable
to prompt injection overall.
```

### attack-surface

```
Go look at everything I have deployed across all my projects, hosts, vendors, sites,
and technologies, and come up with a comprehensive list we will keep in attacksurface.md
as a running, continuously updated resource. For each thing I want to understand: what
tech it uses, whether it is self-hosted or third-party, how we authenticate into it,
the common security issues and misconfigurations for that platform, everything we have
deployed there, and whether it is a web property, a database, or an API, the total
attack surface for that system. What security mechanisms have we defended it with, and
what exposure does each service have to which audiences: public, internal, behind VPN,
token required, OAuth? Recommend a testing frequency for each based on criticality
and cost.
```

---

## LIFE

### big-picture

```
Take a look at all my various projects and writing online, all the activities we have
been doing in the harness, and everything you know about me from web search, and analyze
it deeply. Then look at what is going on in my field, in AI, and in society and the
future in general, and tell me what solves the Japanese concept of ikigai for me. What
should I be working on that gives me fulfillment but is also lucrative, doing it for
myself, with collaborators, or working for a corporation? Make concrete recommendations
if you have them, and feel free to interview me for more context before creating the
output. The goal is to clear up the chaos of my scattered projects and get me focused
in a single direction.
```

### most-wrong

```
Take everything you know about me, my plans, and my biggest current bets, and turn on
me. Steelman the case that my largest bet is wrong. Surface the load-bearing beliefs my
decisions rest on that I have never actually checked. And tell me what evidence would
change my mind, and whether I would even notice it if I saw it.
```

### 10x-or-dies

```
Given where frontier AI is actually heading, tell me which parts of my work and life
are about to go obsolete, and which are about to 10x. Separate what I should stop
investing in now from what I should pour myself into. And give me the specific changes
to make this year, not someday.
```

### decisions-into-policy

```
Find the decisions I make over and over, and stop me from re-litigating them. Surface
the choices I remake from scratch every time and the latent rule behind each. Sort them
by reversibility and stakes, where I am slow on cheap reversible calls and reckless on
expensive irreversible ones. Then turn each one into a standing policy I can run on
autopilot.
```

### binding-constraint

```
Out of everything limiting my life and work, find the single binding constraint, the
actual bottleneck, not the loudest problem. Show me where I am pouring effort into
things that are not the constraint. And tell me the one move that relieves it, and what
becomes possible once it is gone.
```

### bus-factor

```
If I vanished for 30 days, tell me what breaks, and what only keeps running because it
lives in my head and never in the system. Name every undocumented dependency and
me-shaped hole in how my life and work run. Then give me the plan to get the
load-bearing stuff out of my head and into something durable.
```

---

## APPENDIX (extras from the same article, use only on explicit request)

### maintenance-loop (Peter Steinberger's loop prompt)

```
While repository maintenance is active, wake every five minutes. Triage repositories and
read each repository thread's latest state. Reuse one thread per repository; assign its
highest-value bounded task only within granted permissions, and do not interrupt coherent
active work. Require tests, live proof, autoreview, and green CI before any work can
land. Escalate product, access, security, or irreversible decisions. Record meaningful
changes, and stop when every item is landed, decision-ready, blocked, or has no work left.
```

### blog-consolidation

```
Go find everything I have written online since I started writing on the internet, across
all platforms and social media accounts, and unify it into my permanent blog under my
permanent domain. Look at that domain, and if it is a good one for a permanent location,
keep it; if you think I should use a different one, recommend options based on my content
and everything you know about me. Ultimately I need everything consolidated into a single
location, with a single host, at a single domain, so my ideas, projects, and content do
not disappear as platforms come and go.
```
