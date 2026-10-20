# Paper — InteractAgent: Agentic Human Motion Interaction with Memory-Augmented Reflection

- **Paper:** http://arxiv.org/abs/2610.25649v1
- **PDF:** https://arxiv.org/pdf/2610.25649v1
- **Discovered on:** 2026-10-20
- **Code status:** candidates_found
- **Code URL:** https://github.com/Aaron617/agent-arXiv-daily

## Summary

Long-horizon human-scene interaction requires coordinated spatial reasoning, physical feasibility, and the ability to recover from compounding execution errors. Text-driven motion models are largely scene-agnostic and lack closed-loop correction, while geometry-conditioned approaches depend on paired scene-motion training or explicit 3D preprocessing that limits generalization to novel layouts and open-vocabulary goals. We present InteractAgent, an agentic multimodal LLM system for long-horizon human-scene interaction that plans, executes, observes, and reflects in a closed loop, using a single MLLM as both planner and evaluator and a frozen MotionLLM as the executor. InteractAgent integrates Online Observation for step-wise recovery decisions (continue/redo/replan) and Memory-Augmented Reflection for multi-round plan refinement with adaptive stopping. On UniHSI, InteractAgent improves task success and reduces penetration compared with training-free baselines. Code: https://github.com/AIGeeksGroup/InteractAgent.
