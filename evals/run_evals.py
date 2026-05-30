import os
import statistics
import sys
import time

# ensure project root is on sys.path when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands.models.anthropic import AnthropicModel
from strands_evals import Case, Experiment, eval_task, TracedHandler
from strands_evals.evaluators import Contains, OutputEvaluator, ToolCalled

from agent import create_agent
from evals.eval_cases import EVAL_CASES

_latencies: list[float] = []


class _TimedTracedHandler(TracedHandler):
    """TracedHandler that also records wall-clock latency per case."""

    def before(self, case: Case) -> None:
        super().before(case)
        self._t0 = time.perf_counter()

    def after(self, case: Case, result) -> dict:
        _latencies.append((time.perf_counter() - self._t0) * 1000)
        return super().after(case, result)


@eval_task(_TimedTracedHandler())
def _run_case(case: Case) -> object:
    # Returning a fresh Agent lets eval_task invoke it with case.input automatically,
    # ensuring no conversation history leaks between eval cases.
    return create_agent()


def main() -> None:
    eval_model = AnthropicModel(
        model_id=os.environ.get("ANTHROPIC_MODEL_ID", "claude-3-5-sonnet-20241022"),
        max_tokens=512,
    )

    evaluators = [
        # Deterministic (free) — no LLM judge needed
        Contains(),          # expected_output string appears in response
        ToolCalled("count_char"),  # the right tool was invoked
        # LLM judge — rates response quality against a rubric
        OutputEvaluator(
            model=eval_model,
            rubric=(
                "Score 1.0: response states the exact correct count clearly.\n"
                "Score 0.5: correct count present but explanation is confusing.\n"
                "Score 0.0: wrong count or refuses to answer."
            ),
        ),
    ]

    experiment = Experiment(cases=EVAL_CASES, evaluators=evaluators)
    reports = experiment.run_evaluations(_run_case)

    for report in reports:
        report.run_display()

    if _latencies:
        sorted_lat = sorted(_latencies)
        p95_idx = max(0, int(len(sorted_lat) * 0.95) - 1)
        print("\nPerformance:")
        print(f"  Min : {min(_latencies):.0f} ms")
        print(f"  Avg : {statistics.mean(_latencies):.0f} ms")
        print(f"  P95 : {sorted_lat[p95_idx]:.0f} ms")


if __name__ == "__main__":
    main()
