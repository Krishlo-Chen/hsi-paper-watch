# Paper — MaMi-HOI: Harmonizing Global Kinematics and Local Geometry for Human-Object Interaction Generation

- **Paper:** http://arxiv.org/abs/2605.05756v1
- **PDF:** https://arxiv.org/pdf/2605.05756v1
- **Discovered on:** 2026-05-17
- **Code status:** candidates_found
- **Code URL:** https://github.com/Foruck/Awesome-Human-Motion

## Summary

Generating realistic 3D Human-Object Interactions (HOI) is a fundamental task for applications ranging from embodied AI to virtual content creation, which requires harmonizing high-level semantic intent with strict low-level physical constraints. Existing methods excel at semantic alignment, however, they struggle to maintain precise object contact. We reveal a key finding termed \textit{Geometric Forgetting}: as diffusion model depth increases, semantic feature tend to overshadow object geometry feature, causing the model to lose its perception to object geometry. To address this, we propose MaMi-HOI, a hierarchical framework reconciling \textbf{Ma}cro-level kinematic fluidity with \textbf{Mi}cro-level spatial precision. First, to counteract geometric forgetting, we introduce the Geometry-Aware Proximity Adapter (GAPA), which explicitly re-injects dense object details to perform residual snapping corrections for precise contact. Nevertheless, such aggressive local enforcement can disrupt global dynamics, leading to robotic stiffness. In response, we introduce the Kinematic Harmony Adapter (KHA), which proactively aligns whole-body posture with spatial objectives, ensuring the skeleton actively accommodates constraints without compromising naturalness. Extensive experiments validate that MaMi-HOI simultaneously achieves natural motion and precise contact. Crucially, it extends generation capabilities to long-term tasks with complex trajectories, effectively bridging the gap between global navigation and high-fidelity manipulation in 3D scenes. Code is available at https://github.com/DON738110198/MaMi-HOI.git
