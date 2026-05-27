# Paper — InHabit: Leveraging Image Foundation Models for Scalable 3D Human Placement

- **Paper:** http://arxiv.org/abs/2604.19673v2
- **PDF:** https://arxiv.org/pdf/2604.19673v2
- **Discovered on:** 2026-05-27
- **Code status:** candidates_found
- **Code URL:** https://github.com/BaiShuanghao/my_arXiv_daily

## Summary

Training embodied agents to understand 3D scenes as humans do requires large-scale data of people meaningfully interacting with diverse environments, yet such data is scarce. Real-world capture is costly and limited to controlled settings, while existing synthetic datasets rely on simple geometric heuristics, ignoring rich scene context. In contrast, 2D foundation models trained at internet scale have acquired commonsense knowledge of human-environment interactions. To transfer this knowledge to 3D, we introduce InHabit, an automatic and scalable data generator for populating 3D scenes with interacting humans. InHabit follows a render-generate-lift principle: given a rendered 3D scene, a vision-language model proposes contextually meaningful actions, an image-editing model inserts a human, and an optimization procedure lifts the edited result into physically plausible SMPL-X bodies aligned with the scene geometry. Applied to Habitat-Matterport3D, InHabit produces InHabitants, the first large-scale photorealistic 3D human-scene interaction dataset, with 78K samples across $\sim$800 building-scale scenes with complete 3D geometry, SMPL-X bodies, and images. Augmenting standard training data with InHabitants improves RGB-based 3D human-scene reconstruction and contact estimation, and in a perceptual user study our data is preferred in 78% of cases over prior art.
