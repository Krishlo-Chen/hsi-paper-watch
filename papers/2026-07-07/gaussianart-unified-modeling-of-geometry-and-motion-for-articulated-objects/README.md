# Paper — GaussianArt: Unified Modeling of Geometry and Motion for Articulated Objects

- **Paper:** http://arxiv.org/abs/2508.14891v3
- **PDF:** https://arxiv.org/pdf/2508.14891v3
- **Discovered on:** 2026-07-07
- **Code status:** candidates_found
- **Code URL:** https://github.com/shenlc19/GaussianArt

## Summary

Reconstructing articulated objects is essential for building digital twins of interactive environments. However, prior methods typically decouple geometry and motion by first reconstructing object shape in distinct states and then estimating articulation through post-hoc alignment. This separation complicates the reconstruction pipeline and restricts scalability, especially for objects with complex, multi-part articulation. We introduce a unified representation that jointly models geometry and motion using articulated 3D Gaussians. This formulation improves robustness in motion decomposition and supports articulated objects with up to 20 parts, significantly outperforming prior approaches that often struggle beyond 2--3 parts due to brittle initialization. To systematically assess scalability and generalization, we propose MPArt-90, a new benchmark consisting of 90 articulated objects across 20 categories, each with diverse part counts and motion configurations. Extensive experiments show that our method consistently achieves superior accuracy in part-level geometry reconstruction and motion estimation across a broad range of object types. We further demonstrate applicability to downstream tasks such as robotic simulation and human-scene interaction modeling, highlighting the potential of unified articulated representations in scalable physical modeling.
