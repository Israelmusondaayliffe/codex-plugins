# Prompt benchmark design

Success cases represent the main user job and normal inputs.
Boundary cases test near-misses, ambiguous inputs, long context, tool limits, or partial evidence.
Failure cases test malformed inputs, unsupported parameters, missing tools, and safe refusal or handoff behavior.

Assertions should be observable and discriminating. Record model, prompt version, tool access, temperature or effort settings when supported, and whole-session usage separately from marginal prompt cost.

