"""PCGrad on a shared trunk, preserving task-specific gradients before global clipping.

The default sum reduction matches the weighted summed multi-task objective.
Local projection does not guarantee improved test error or conflict-free AdamW updates.
"""
from __future__ import annotations

import random
from collections.abc import Iterable
import torch


def project_two_gradients(g1, g2, enabled=True):
    """Project both vectors against the original other vector, never an updated one."""
    if g1.ndim != 1 or g1.shape != g2.shape:
        raise ValueError("Expected matching gradient vectors")
    if not torch.isfinite(g1).all() or not torch.isfinite(g2).all():
        raise ValueError("Nonfinite task gradients")
    dot = torch.dot(g1, g2)
    norm1, norm2 = torch.dot(g1, g1), torch.dot(g2, g2)
    conflict = bool(dot < 0)
    a, b = g1.clone(), g2.clone()
    if enabled and conflict:
        if norm1 <= 0 or norm2 <= 0:
            raise RuntimeError("Negative dot product with zero gradient norm")
        a = g1-(dot/norm2)*g2
        b = g2-(dot/norm1)*g1
    denominator = torch.sqrt(norm1*norm2)
    cosine = float(dot/denominator) if denominator > 0 else 0.
    stats = {"dot": float(dot), "cosine": cosine, "conflict": conflict,
             "task1_norm": float(torch.sqrt(norm1)), "task2_norm": float(torch.sqrt(norm2)),
             "projected": bool(enabled and conflict)}
    return a, b, stats


class PCGradOptimizer:
    """Optimizer wrapper for a common trunk with private task heads.

    shared_params=None infers parameters connected to every loss. Partial sharing
    across only some of three or more tasks is rejected rather than misinterpreted.
    Explicit shared_params must be connected to every task. Mean reduction applies
    only to shared gradients; private gradients remain direct task gradients.
    """
    def __init__(self, base_optimizer, num_tasks=2, reduction="sum",
                 shared_params: Iterable[torch.nn.Parameter] | None = None, seed=0):
        if num_tasks < 2 or reduction not in ("sum", "mean"):
            raise ValueError("Require at least two tasks and sum/mean reduction")
        self._optim = base_optimizer
        self.num_tasks = num_tasks
        self.reduction = reduction
        self.param_groups = base_optimizer.param_groups
        self.state = base_optimizer.state
        self._params = [p for group in self.param_groups for p in group["params"] if p.requires_grad]
        if len({id(p) for p in self._params}) != len(self._params):
            raise ValueError("Duplicate optimizer parameters")
        self._shared_ids = None if shared_params is None else {id(p) for p in shared_params}
        if self._shared_ids is not None and not self._shared_ids.issubset({id(p) for p in self._params}):
            raise ValueError("Shared parameters must belong to optimizer")
        self._rng = random.Random(seed)
        self.last_stats = {}
        self.last_witness = None

    def pc_backward(self, losses, project=True, capture=False):
        if len(losses) != self.num_tasks:
            raise ValueError(f"Expected {self.num_tasks} losses")
        if any(loss.ndim != 0 or not torch.isfinite(loss) for loss in losses):
            raise ValueError("Losses must be finite scalars")
        self.zero_grad()
        grads = [torch.autograd.grad(loss, self._params, retain_graph=i < len(losses)-1,
                                     allow_unused=True) for i, loss in enumerate(losses)]
        shared_indices = []
        for i, parameter in enumerate(self._params):
            connected = sum(g[i] is not None for g in grads)
            shared = (connected == self.num_tasks if self._shared_ids is None
                      else id(parameter) in self._shared_ids)
            if shared and connected != self.num_tasks:
                raise ValueError("An explicit shared parameter is not connected to all tasks")
            if not shared and 1 < connected < self.num_tasks:
                raise ValueError("Partially shared parameter blocks require explicit handling")
            if shared:
                shared_indices.append(i)
        flat = [torch.cat([g[i].detach().reshape(-1) for i in shared_indices])
                if shared_indices else torch.empty(0, device=self._params[0].device)
                for g in grads]
        if self.num_tasks == 2:
            a, b, self.last_stats = project_two_gradients(flat[0], flat[1], enabled=project)
            projected = [a, b]
        else:
            projected = []
            for i, gi in enumerate(flat):
                updated = gi.clone()
                order = [j for j in range(self.num_tasks) if j != i]
                self._rng.shuffle(order)
                for j in order:
                    dot = torch.dot(updated, flat[j])
                    if project and dot < 0:
                        updated = updated-dot/torch.dot(flat[j], flat[j])*flat[j]
                projected.append(updated)
            self.last_stats = {"projected": bool(project)}
        combined = torch.stack(projected).sum(dim=0)
        if self.reduction == "mean":
            combined = combined/self.num_tasks
        offset = 0
        shared_set = set(shared_indices)
        for i, parameter in enumerate(self._params):
            if i in shared_set:
                parameter.grad = combined[offset:offset+parameter.numel()].view_as(parameter).clone()
                offset += parameter.numel()
            else:
                connected_grads = [g[i].detach() for g in grads if g[i] is not None]
                parameter.grad = (torch.stack(connected_grads).sum(dim=0)
                                  if connected_grads else None)
        self.last_witness = None
        if capture:
            self.last_witness = {
                "shared_parameter_indices": shared_indices,
                "parameter_shapes": [list(p.shape) for p in self._params],
                "task_gradient_presence": [[g is not None for g in task] for task in grads],
                "task_gradients": [torch.cat([(torch.zeros_like(p) if g is None else g).detach().reshape(-1)
                                              for p, g in zip(self._params, task)]).cpu() for task in grads],
                "projected_shared_gradients": [g.cpu().clone() for g in projected],
                "assigned_gradient": torch.cat([(torch.zeros_like(p) if p.grad is None else p.grad).reshape(-1)
                                                for p in self._params]).detach().cpu(),
                "project_enabled": project, "stats": self.last_stats.copy(),
                "reduction": self.reduction}

    def step(self, closure=None):
        return self._optim.step(closure)

    def zero_grad(self, set_to_none=True):
        self._optim.zero_grad(set_to_none=set_to_none)

    def state_dict(self):
        return self._optim.state_dict()

    def load_state_dict(self, state_dict):
        self._optim.load_state_dict(state_dict)
