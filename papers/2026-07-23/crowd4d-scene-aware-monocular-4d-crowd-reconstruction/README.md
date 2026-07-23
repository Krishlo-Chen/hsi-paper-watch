# Paper — Crowd4D: Scene-Aware Monocular 4D Crowd Reconstruction

- **Paper:** http://arxiv.org/abs/2607.19517v1
- **PDF:** https://arxiv.org/pdf/2607.19517v1
- **Discovered on:** 2026-07-23
- **Code status:** candidates_found
- **Code URL:** https://github.com/KHB1698/DyCrowd

## Summary

Recovering scene-consistent 4D crowd motion from monocular video in large-scale scenes remains challenging due to severe depth ambiguity and complex scene geometry. Existing monocular crowd reconstruction methods typically rely on single-plane assumptions, leading to unreliable metric scale and spatial drift under complex terrain. We propose Crowd4D, the first scene-aware 4D crowd reconstruction framework that jointly optimizes the crowd and scene from a monocular RGB video in large-scale scenes. Crowd4D explicitly incorporates scene geometry and ensures consistency across image and scene spaces via a multi-stage optimization strategy. A key bottleneck of this task lies in accurate human-scene alignment, particularly in scale and position. However, human and scene reconstructions are typically decoupled. To address this, we introduce the Human-Scene Interaction Proxy, abbreviated as HSIP, as an intermediate representation derived from Scene Interaction Point Clouds and a Scene Interaction Surface, abbreviated as SIPC and SIS. These representations encode explicit scene-aware geometric priors and redefine the optimization space for large-scale monocular 4D crowd reconstruction. To further improve temporal stability under occlusions, we introduce Crowd Structural Coherence Regularization, abbreviated as CSCR, which leverages HSIP-based spatial priors to impose soft temporal consistency on pairwise relative displacements and directions within local crowd neighborhoods. Extensive experiments demonstrate that Crowd4D consistently outperforms existing state-of-the-art methods and enables robust monocular 4D crowd reconstruction in complex, large-scale real-world scenes.
