# Paper — AccioScene: Compositional 3D Scene Generation via Graph Diffusion and Interaction-driven Critics

- **Paper:** http://arxiv.org/abs/2502.06819v2
- **PDF:** https://arxiv.org/pdf/2502.06819v2
- **Discovered on:** 2026-06-09
- **Code status:** not_confirmed
- **Code URL:** not confirmed

## Summary

This paper presents a framework for generating 3D indoor scenes from text prompts. Existing methods often formulate scene synthesis as an object layout prediction problem conditioned on a single input modality, such as a text description, room shape, or scene graph. This design can lead to object collisions and limited functional plausibility, reducing its practical applicability. To address these limitations, we introduce a multi-stage pipeline that better reflects practical scene creation scenarios. Given a text prompt describing partial scene content, our method first uses graph diffusion to produce a contextually coherent scene graph and then predicts a realistic object layout. In addition, we incorporate lightweight human-object interaction priors to encourage human-centric and functional arrangements, with explicit spatial constraints to reduce interpenetration. Our approach generates coherent 3D scenes with viable layouts that better support human interaction. Experiments on the 3D-FRONT dataset demonstrate that our method achieves competitive or state-of-the-art performance compared with existing approaches, while improving the physical plausibility of generated scenes.
