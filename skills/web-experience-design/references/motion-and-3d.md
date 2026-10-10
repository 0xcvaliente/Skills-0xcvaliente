# Motion and 3D

Read this reference when a page needs motion as part of its explanation, a scroll story, or real-time 3D. For a normal interface, keep motion small and use the project's existing animation approach.

## Choose the mechanism

| Need | First option | Escalate when |
| --- | --- | --- |
| State feedback or entrance | CSS transition or the project's motion library | Sequencing or interruption needs explicit control |
| Scroll-linked story | One progress source driving transforms and opacity | Pinning, reversibility, or a multi-beat timeline needs a dedicated tool |
| Object reveal | Images, video, or layered DOM | Real geometry, lighting, or user-controlled viewpoint is essential |
| Real-time 3D | Existing Three/WebGL stack and local assets | New renderer is justified by the brief and device budget |

Use the actual project stack. If GSAP is already chosen, use its timeline or ScrollTrigger where they simplify ownership, cleanup, and scroll progress. A library choice is an implementation decision, not a default aesthetic.

## Story contract

Define one signature moment before coding:

1. **Opening:** What is visible and understood before movement?
2. **Transformation:** What changes, and why does that reveal the subject?
3. **Readable hold:** Where can the user pause and read or act?
4. **Exit:** What stable composition remains, and where does the next action lead?

Specify a mobile composition and static version at the same time. Build and inspect this full beat before adding other effects. Keep a complete visible frame at sampled scroll positions; reversals should restore earlier states. Time-driven ambience must not obscure the scroll-driven change.

## Implementation invariants

- Use one owner for each animated property and one authoritative scroll progress source. Clean up listeners, observers, timelines, render loops, and assets owned by the component.
- Keep layout geometry separate from moving children, especially in pinned sections. Prefer transforms and opacity for frequent updates; avoid layout or paint work on every scroll frame.
- Preserve semantic content, focus order, text selection, and actionable links beneath enhancement. Do not hide essential copy to manufacture a reveal.
- Let reduced motion remove pinning, parallax, smoothing, autoplay, and continuous loops while keeping content and actions usable. Respond if the preference changes while the page is open.
- Gate pointer effects to suitable input devices. Compose mobile with shorter travel and fewer simultaneous layers instead of shrinking desktop choreography.
- For 3D, manage asset loading, render demand or frame budget, resize, context loss, and disposal. Provide a useful static composition for unsupported devices or renderer failure. If the user requested real-time 3D, a poster alone does not complete that request.
