# Data Storytelling Studio

Data Storytelling Studio turns checked analysis into a decision-facing artifact without quietly recalculating or overstating the source evidence.

## Owned workflow

1. `analysis-to-story-router` selects the delivery format and declares the required companion tools.
2. `chart-message-audit` tests each visual claim against its stated evidence and records revisions.
3. `executive-readout-builder` creates an answer-first narrative with decisions, risks, caveats, and next actions.

## Companion boundary

The plugin coordinates installed analytical and publishing capabilities. It does not copy or replace Spreadsheets, Presentations, Visualize, Sites, Writing Quality, or Knowledge Work Superpowers. Data Analytics is an optional companion and must be installed separately if its specialist workflows are needed.

Run `python3 scripts/check_companions.py` before a workflow whose output depends on a companion. Run `python3 scripts/verify_bundle.py` before installation or release.

## Maintenance

Edit the source under `plugins/data-storytelling-studio`, increment the version in both JSON contracts, validate every coordinator template, then reinstall through this marketplace. Do not edit the installed cache.
