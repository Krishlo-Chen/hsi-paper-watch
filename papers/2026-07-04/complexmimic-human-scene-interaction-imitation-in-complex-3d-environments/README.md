# Paper — ComplexMimic: Human-Scene Interaction Imitation in Complex 3D Environments

- **Paper:** http://arxiv.org/abs/2607.02034v1
- **PDF:** https://arxiv.org/pdf/2607.02034v1
- **Discovered on:** 2026-07-04
- **Code status:** candidates_found
- **Code URL:** https://github.com/BaiShuanghao/my_arXiv_daily

## Summary

Physics-based Human-Scene Interaction (HSI) imitation learning is crucial for embodied intelligence as it bridges the gap between kinematic 3D motions and real-world dynamics. However, most existing methods focus on simplified scene settings, leaving complex environments largely unexplored, which limits their applicability in real-world scenarios. In this paper, we focus on HSI mimicry in complex environments. Under this complex setting, we observe an inherent trade-off between successfully performing interaction and maintaining natural, physically plausible motions. To address this challenge, we propose ComplexMimic, a framework that reconstructs diverse HSI by interpreting imperfect MoCap data. First, we introduce a Dual Flow Strategy, which learns two complementary experts: an imitation expert for accurate motion tracking and an interaction expert for collision-aware adaptation in complex scenes. Second, naive multi-expert distillation, which treats all experts equally, often under-samples challenging behaviors, limiting effective learning. To mitigate this issue, we propose a difficulty-aware distillation strategy that adaptively weights supervision and prioritizes hard-yet-learnable trajectories guided by failure statistics and learning progress signals. Extensive experiments on three benchmark datasets demonstrate that our approach outperforms current state-of-the-art methods. Our implementation is available at https://github.com/LuPan23/ComplexMimic.
