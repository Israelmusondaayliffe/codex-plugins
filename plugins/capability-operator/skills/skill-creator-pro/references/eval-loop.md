# Eval Loop: Running, Grading, and Iterating

The core improvement cycle for skills. Draft, run, grade, review, improve, repeat.

---

## Workspace Organization

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Organize by iteration and test case:

```
my-skill-workspace/
├── iteration-1/
│   ├── eval-form-filling/
│   │   ├── with_skill/
│   │   │   └── outputs/
│   │   ├── without_skill/       # baseline
│   │   │   └── outputs/
│   │   └── eval_metadata.json
│   ├── eval-table-extraction/
│   │   ├── with_skill/outputs/
│   │   ├── without_skill/outputs/
│   │   └── eval_metadata.json
│   ├── benchmark.json
│   └── feedback.json
├── iteration-2/
│   └── ...
└── history.json
```

Create directories as you go, not upfront.

---

## Step 1: Spawn All Runs

For each test case, run two versions in the same turn if subagents are available. Do not run with-skill first and come back for baselines later. Launch everything at once.

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

**Baseline run** depends on context:
- **Creating a new skill:** No skill at all. Same prompt, no skill path, save to `without_skill/outputs/`.
- **Improving an existing skill:** The old version. Snapshot the skill first (`cp -r <skill-path> <workspace>/skill-snapshot/`), point baseline at the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case with descriptive name. See `references/schemas.md` for the exact schema.

---

## Step 2: Draft Assertions While Runs Execute

Use wait time productively. Draft quantitative assertions for each test case and explain them to the user.

**Good assertions are:**
- Objectively verifiable (not subjective quality judgments)
- Discriminating (pass when skill succeeds, fail when it doesn't)
- Named descriptively (readable at a glance in the benchmark viewer)

**Avoid:**
- Assertions trivially satisfied (checking filename existence but not content)
- Forcing assertions onto subjective skills (writing style, design quality). These are better evaluated qualitatively by the user.

Update `eval_metadata.json` and `evals/evals.json` with assertions once drafted.

---

## Step 3: Capture Timing Data

When each subagent task completes, the notification includes `total_tokens` and `duration_ms`. Save immediately to `timing.json` in the run directory. This is the only chance to capture this data.

---

## Step 4: Grade, Aggregate, Launch Viewer

Once all runs complete:

### 4A: Grade Each Run

Spawn a grader subagent (or grade inline) that reads `agents/grader.md` and evaluates each assertion against outputs. Save results to `grading.json` in each run directory.

For assertions checkable programmatically, write and run a script. Scripts are faster, more reliable, and reusable across iterations.

### 4B: Aggregate Into Benchmark

Run the aggregation script:
```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <n>
```

Produces `benchmark.json` and `benchmark.md` with pass_rate, time, tokens for each configuration, with mean +/- stddev and delta.

### 4C: Launch the Viewer

```bash
nohup python <skill-creator-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  > /dev/null 2>&1 &
VIEWER_PID=$!
```

For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

**Headless environments:** Use `--static <output_path>` to write a standalone HTML file instead of starting a server.

Always use generate_review.py. Do not write custom HTML.

### What the User Sees

The "Outputs" tab shows one test case at a time: prompt, output files rendered inline, previous iteration output (collapsed), formal grades (collapsed), feedback textbox, and previous feedback.

The "Benchmark" tab shows stats summary: pass rates, timing, token usage for each configuration, per-eval breakdowns, and analyst observations.

Navigation via prev/next buttons or arrow keys. "Submit All Reviews" saves all feedback to `feedback.json`.

---

## Step 5: Read Feedback

When the user finishes reviewing, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "chart missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means the user thought it was fine. Focus improvements on test cases with specific complaints.

Kill the viewer server when done:
```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improving the Skill

This is the heart of the loop. You have test results, user feedback, and benchmark data. Now make the skill better.

### How to Think About Improvements

**1. Generalize from the feedback.** Skills get used across many different prompts. Here you iterate on a few examples because it helps move faster. But if the skill only works for those examples, it's useless. Rather than fiddly overfitty changes or oppressively constrictive MUSTs, try branching out with different metaphors or recommending different patterns. It's relatively cheap to try.

**2. Keep the prompt lean.** Remove things that aren't pulling their weight. Read the transcripts, not just the final outputs. If the skill makes the model waste time doing unproductive things, get rid of those parts and see what happens.

**3. Explain the why.** Try hard to explain the reasoning behind everything you ask the model to do. Current LLMs are smart. They have good theory of mind and when given a good harness can go beyond rote instructions. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag. Reframe and explain the reasoning so the model understands why the thing matters. That's more powerful and effective than shouting.

**4. Look for repeated work across test cases.** Read the transcripts and notice if all test runs independently wrote similar helper scripts or took the same multi-step approach. If all 3 test cases resulted in writing a `create_docx.py`, that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, save every future invocation from reinventing the wheel.

### The Iteration Loop

After improving:

1. Apply improvements to the skill
2. Rerun all test cases into `iteration-<N+1>/`, including baseline runs. For new skills, baseline is always `without_skill`. For improving existing skills, use judgment on whether to compare against the original version or previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for user review
5. Read new feedback, improve again, repeat

**Stop when:**
- User says they're happy
- Feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind Comparison

For rigorous A/B comparison between two skill versions. Read `agents/comparator.md` and `agents/analyzer.md` for details.

The basic idea: give two outputs to an independent agent without telling it which is which, let it judge quality. Then analyze why the winner won.

This is optional and most users won't need it. The human review loop is usually sufficient. Requires subagents.
