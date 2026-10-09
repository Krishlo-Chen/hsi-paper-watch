# Paper — MAMHOI: Factorizing Scene-Aware Human-Object Interaction through Affordances

- **Paper:** http://arxiv.org/abs/2610.12416v1
- **PDF:** https://arxiv.org/pdf/2610.12416v1
- **Discovered on:** 2026-10-09
- **Code status:** candidates_found
- **Code URL:** https://github.com/InsomaniacElf/sg-tamil-tts-resources-

## Summary

Generating realistic human-object interactions (HOI) in complex 3D scenes requires two complementary capabilities: reasoning about interaction feasibility in the environment and synthesizing realistic human-object motion. However, supervision for these capabilities is rarely available jointly at scale. Human-scene datasets provide rich information about environment-aware motion, while human-object datasets capture detailed interaction dynamics, yet paired human-object-scene data remain scarce. We present MAMHOI, an affordance-mediated factorization for scene-aware human-object interaction generation. MAMHOI factorizes scene-aware HOI generation through an explicit motion-affordance interface between scene understanding and motion synthesis: a scene-conditioned model first predicts where and how an interaction can be feasibly executed, and an affordance-conditioned HOI model then generates the corresponding human-object motion. This factorization allows scene understanding and interaction dynamics to be learned from complementary sources of supervision without requiring paired human-object-scene data. Experiments in complex indoor environments show that MAMHOI reduces object--scene penetration while better preserving human--object interaction quality, yielding more realistic and physically feasible scene-aware interactions. Project page: https://leimingyuan.github.io/MAMHOI-project-page/
