# Visual Review of Captures

Read when reviewing a UI change or capturing named states. This adds image inspection to the existing probes; it does not introduce a persistent pixel-baseline service or a second route map.

## Comparable evidence

Hold target selection, viewport, theme, fixture data, clock, font readiness, and motion settings the same for the before and after captures. Record the source revision and any uncommitted edits for each run. Prefer an isolated checkout of the base revision; never swap the source under a live dev server in the middle of a capture. For a deployed build, record the build identity the server reports instead of assuming the URL points at the intended commit; a build with no identity leaves that claim unverified.

Keep both sets of captures. A narrower rerun must not overwrite a broader earlier set, because missing frames would then read as new UI. New UI can have after-only evidence: say the baseline is missing rather than inventing one. A change to a shared component needs its affected consumers captured, not only the files a directory glob happens to match.

## Inspect, then report

Open the captured images with whatever image-viewing capability the session has. Look at every changed state in the scoped set, plus nearby unchanged areas that might already be broken. Report the intended visual change, any unexpected differences, and exactly which captures were inspected. A successful screenshot command or a passing functional test cannot establish alignment, clipping, stacking order, or visual correctness. Captures nobody opened are listed as unreviewed.

If an image-diff tool exists, use it to prioritise which frames to open, but still inspect the rendered frame and not only its diff. Freeze sources of variability, or mask a named volatile region; never loosen the threshold until a defect disappears. Record every mask, since a masked region is untested. A claim about motion needs a recording or frame sequence captured with motion enabled.

For a visible defect, attach the image and add a focused measurement where one is possible, such as the bounding boxes of a checkbox and its label. Keep visual observations apart from measured rule results. Subjective design judgment and severity stay with `ui-design`; a capture review assigns no ship verdict.

## Suspicious duplicates

When adding capture coverage or named states, compare frames that should differ under identical capture conditions. Prefer decoded-pixel equality including dimensions; PNG file hashes can differ from metadata or encoding alone while the pixels match, and can match less often than the pixels do. With no comparator available, compare side by side and label the check manual instead of claiming an automated sweep.

For each group of identical frames, confirm the state precondition: did the dialog open, did the loading fixture activate, did the theme attribute change? Assert the distinguishing state before recapturing. Identical pixels can be intentional, such as a monochrome logo in two themes; record that explanation. A fixture that never activated is a harness failure, not evidence of an app defect. A state that cannot be reached stays unknown.
