"""Task-local BDD model portable between SpecWeave, Taskledger, and JSON.

This package owns a neutral representation of task BDD (rules + examples) that is
independent of Taskledger task state. It does not replace Taskledger lifecycle;
it is a portable representation Taskledger can export/import or that SpecWeave
can read from JSON/YAML.
"""

from specweave.bdd.convert import feature_to_task_bdd, task_bdd_to_feature
from specweave.bdd.model import BddExample, BddRule, TaskBddSpec
from specweave.bdd.store import load_task_bdd_json, save_task_bdd_json

__all__ = [
    "BddExample",
    "BddRule",
    "TaskBddSpec",
    "feature_to_task_bdd",
    "task_bdd_to_feature",
    "load_task_bdd_json",
    "save_task_bdd_json",
]
