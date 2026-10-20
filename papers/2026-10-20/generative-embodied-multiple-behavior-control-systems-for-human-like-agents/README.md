# Paper — Generative Embodied Multiple Behavior Control Systems for Human-like Agents

- **Paper:** http://arxiv.org/abs/2609.22691v3
- **PDF:** https://arxiv.org/pdf/2609.22691v3
- **Discovered on:** 2026-10-20
- **Code status:** candidates_found
- **Code URL:** https://github.com/Nicolas99-9/llm-agent-simulation-papers

## Summary

Building autonomous agents that reproduce human behavior in realistic 3D environments has been a longstanding objective in AI. Cognitive neuroscience commonly believes that human behaviors are controlled by multiple control systems including goal-directed and habitual. However, existing human-like agent frameworks primarily focus on goal-directed system and habitual system is largely overlooked. In this paper, we address this gap by proposing GEMS, a Generative Embodied Multiple Behavior Control System that jointly models goal-directed and habitual behaviors for generating believable human-like behavior. GEMS employs a cognitive module to generate natural language behaviors and a motion generation module to construct them in 3D environment. The cognitive module comprises a Habitual Controller that retrieves habitual actions from habit memory in response to environmental stimuli, a Goal-directed Controller that proposes goal-directed actions for current goal, and an Arbiter that governs their influence and selects the final action, supporting diverse and naturalistic behavior patterns generation. To construct these behaviors, the motion generation module adopts a Text-to-Motion model to generate versatile and expressive 3D human-scene interactions without relying on predefined actions. Extensive evaluations, human and ablation studies demonstrate that human-likeness performance is substantially improved by GEMS. The efficacy of GEMS indicates the benefits of leveraging habitual behavior and multiple behavior control system coordination for believable embodied human-like agents design.
