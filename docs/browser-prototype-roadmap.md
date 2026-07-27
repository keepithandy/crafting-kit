# Browser Prototype Structure Roadmap

This roadmap tracks the browser-facing Crafting Kit work. The interface remains a read-only
preview surface while the Python helpers and content contracts remain independent of the UI.

## Issue #18 — Directory structure

- [x] Add `prototype/index.html` as the browser entry point.
- [x] Move presentation into `prototype/styles.css`.
- [x] Move browser state and rendering into `prototype/app.js`.
- [x] Keep `prototype/crafting-interface.html` as a compatibility entry point.
- [x] Preserve recipe selection, inventory display, blocked states, and output preview.
- [x] Document the structure and launch path in the README.
- [x] Commit and publish the structure pass.

## Upcoming issues

- [x] #19 — Build the semantic crafting interface shell (local implementation complete; not yet published).
- [x] #21 — Create the responsive Crafting Kit design system (complete and synchronized).
- [x] #20 — Add the browser state and rendering controller improvements.
- [ ] #22 — Define the content-loading boundary.
- [ ] #23 — Build the recipe browser and requirement detail panel.
- [ ] #24 — Add read-only inventory, batch, capacity, and quality panels.
- [ ] #25 — Complete mobile and accessibility polish.

## Guardrails

- No live crafting mutation.
- No persistence or save integration.
- No timers or crafting queues.
- No random quality rolls.
- No economy tuning.
- No automatic content migration.
- No dedicated tests are added as part of this roadmap phase.
