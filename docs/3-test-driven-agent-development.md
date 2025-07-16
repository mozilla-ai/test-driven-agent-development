# Test Driven (Agent) Development

Now that we have a baseline agent, which we want to improve, we can start exploring how
Test Driven Development can be applied to agent projects.

## What is different when developing agents

In many cases, the non-deterministic nature of AI has been used as an excuse
in AI projects for not writing tests and/or not applying approaches like TDD.

In practice, almost any iteration that we make to improve an agent can be tested
as regular software, without the need of specialized tools or platforms.

## Reusing workflow components and tests

As mentioned before, some of the "good practices" used before are useful when
migrating to an agent.

Because we took care of writing domain-specific tools that do a single thing, have a clear
docstring and simple inputs/outputs, we can directly provide them to the agent:

```python
TOOLS = [
    driving_hours_to_meters,
    get_area_lat_lon,
    get_surfing_spots,
    get_wave_forecast,
    get_wind_forecast,
]
```
Their existing unit tests remain useful in this context.

We can also adapt the existing [`test_workflow.py`](../tests/test_workflow.py) to
have an end-to-end [`test_agent.py`](../tests/test_agent.py):

```python
from datetime import datetime

from any_agent import AgentTrace
from find_surf_spots.agent import find_surf_spots_agent, SurfSpot
from find_surf_spots.tools.openmeteo import DIRECTIONS


def test_find_surf_spots_agent():
    agent_trace: AgentTrace = find_surf_spots_agent("Vigo", datetime.now().isoformat())

    spots = agent_trace.final_output.spots
    assert all(isinstance(r, SurfSpot) for spot in spots)
    assert any(r.name == "Praia de Patos" for spot in spots)
    for spot in spots:
        assert all(f.wave_direction in DIRECTIONS for f in spot.wave_forecast)
        assert all(f.wind_direction in DIRECTIONS for f in spot.wind_forecast)
```

## Agent-specific tests

Compared to our `workflow` solution, the "problem" with that test is that
an agent could pass all those assertions without actually having gone
through the steps that we want.

Luckily, the returned `agent_trace` can be used inside tests exactly for this purpose.

`any-agent` encourages three approaches for evaluating agent traces:

- Custom Code Evaluation: Direct programmatic inspection of traces for deterministic checks
- [LlmJudge](https://mozilla-ai.github.io/any-agent/api/evaluation/#any_agent.evaluation.LlmJudge): LLM-as-a-judge for evaluations that can be answered with a direct LLM call alongside a custom context
- [AgentJudge](https://mozilla-ai.github.io/any-agent/api/evaluation/#any_agent.evaluation.AgentJudge): Complex LLM-based evaluations that utilize built-in and customizable tools to inspect specific parts of the trace or other custom information provided to the agent as a tool

> [!TIP]
> Read more at https://mozilla-ai.github.io/any-agent/evaluation/

We can apply those patterns in our test.

To start simple, we can check if the `get_surfing_spots` tool was used
to get the answer.

-> Check [`test_agent.py`](../tests/test_agent.py)

## Agent baseline

Having our initial test ready and failing, we can go ahead an implement
a first version of the agent.

-> Check [`agent.py`](../src/find_surf_spots/agent.py).

And run the test to see if this basic agent already behaves as expected:

```bash
pytest --disable-warnings -v -s tests/test_agent.py
```

## Iterating on Agents

With the baseline agent and tests ready, we can proceed to iterate on our Agent.

One of the motivations for using an Agent was the idea of browsing the web
for recommended conditions about a spot and comparing that against the forecast.

We can start by extending our test to verify that the agent calls the
`visit_webpage` to fetch the recommended conditions about spots, using the website that we will indicate in the instructions:

```python
def assert_tool_was_used(agent_trace: AgentTrace, tool_name: str, with_args: str = None):
    assert any(
        (
            span.attributes.get(GenAI.TOOL_NAME) == tool_name
            and span.status.status_code.value == "ok"
            and
            (
                with_args in span.attributes.get(GenAI.TOOL_ARGS)
                if with_args is not None
                else True
            )
        )
        for span in agent_trace.spans
        if span.is_tool_execution()
    )


def test_find_surf_spots_agent():
    agent_trace = find_surf_spots_agent("Vigo", datetime.now().isoformat())

    ...

    assert_tool_was_used(agent_trace, "visit_webpage", with_args="surf-forecast.com")
```

With that setup, we can proceed to update the instructions and tools of our agent:

```python
    ...

    INSTRUCTIONS = """
    Use the tools to find an answer.

    Once you have found surfing spots and checked their corresponding forecast,
    you must browse the web to find what are the recommended conditions
    for a spot. A common site to find this information is `surf-forecast.com`.
    """
    TOOLS = [
        driving_hours_to_meters,
        get_area_lat_lon,
        get_surfing_spots,
        get_wave_forecast,
        get_wind_forecast,
        # Generic web browsing tools
        search_tavily,
        visit_webpage
    ]
```

And now we can verify test the changes:

```bash
pytest --disable-warnings -v -s tests/test_agent.py
```
