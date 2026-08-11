# Paper — Efficient Human-Contact Representation for Human-Scene Interaction

- **Paper:** http://arxiv.org/abs/2608.09388v1
- **PDF:** https://arxiv.org/pdf/2608.09388v1
- **Discovered on:** 2026-08-11
- **Code status:** not_confirmed
- **Code URL:** not confirmed

## Summary

Human-scene interaction is an active research topic with several industrial applications in virtual reality, gaming, robotics, and surveillance. Despite significant progress in network architectures to improve the results or optimize models' parameters for fast inference speed, the efficient representation of contact between humans and their environments remains an open challenge. In this paper, we propose a new efficient human-contact representation for human-scene interaction. Our primary contribution is the introduction of sparse contact masks that strategically select essential contact information, significantly reducing redundant data in high-dimensional inputs. Leveraging this efficient contact representation, we propose a suite of sparse operators to replace traditional dense operators within deep network layers for faster computation. Our approach not only enhances computational speed but also filters out non-essential contact data, thereby improving the precision of human-scene interaction models. To validate the effectiveness of our method, we conduct intensive experiments across three public benchmark datasets, focusing on two critical tasks for human-scene interaction: contact prediction and scene synthesis. The experimental results show that our approach outperforms state-of-the-art models in reconstruction accuracy and achieves a computation speed-up of at least 12 times over recent baselines.
