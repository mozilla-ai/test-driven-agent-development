# Defining and Running agents

Once we have identified and verified the need for an agent, we can start
implementing a simple agent as a baseline.

## Defining Agents

Agents are just an LLM with access to tools running in a loop:

```python
history = [instructions, user_prompt]

while True:
    response = CALL_LLM(history)
    history.append(response)
    if response.tool_executions:
        for tool_execution in tool_executions:
            tool_response = EXECUTE_TOOL(tool_execution)
            history.append(tool_response)
    else:
        return response
```

As such, the components that define an Agent behavior are:

- `MODEL_ID`: The underlying model used in the loop.
- `INSTRUCTIONS`: Where we define how we want the agent to behave.
- `TOOLS`: The functions that the LLM can decide to call in the response, based on our instructions.

We will be using https://github.com/mozilla-ai/any-agent in the workshop, which allows
to define and run agents using different agent frameworks under the hood:

```python
from any_agent import AgentConfig, AnyAgent
from any_agent.tools import search_tavily, visit_webpage

MODEL_ID = "gemini/gemini-2.5-flash"
INSTRUCTIONS = "Use the tools to find an answer"
TOOLS = [search_tavily, visit_webpage]

agent = AnyAgent.create(
    "tinyagent",
    AgentConfig(
        model_id=MODEL_ID,
        instructions=INSTRUCTIONS,
        tools=TOOLS
    )
)
```

## Running agents

Once an agent is defined, it can run multiple times with different user prompts:

```python
agent_trace = agent.run("Recommend me surf spots around Vigo for today")
```

```python
agent_trace = agent.run("Recommend me surf spots around Salvaterra de Miño for tomorrow")
```

## Using the returned traces

`any-agent` generates standardized (regarding the structure) [OpenTelemetry](https://opentelemetry.io/) traces regardless of the framework used, based on the [Semantic conventions for generative AI systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/).

Apart from being visible in the output console and available in any OpenTelemetry-compatible exporter, we can use the convenience [`AgentTrace`](https://mozilla-ai.github.io/any-agent/api/tracing/#any_agent.tracing.agent_trace.AgentTrace) returned from the `agent.run` to access both the final output and the steps (called `spans` in OpenTelemetry) followed by the agent:

```
print(agent_trace.final_output)
print(agent_trace.spans[1])
```

We can use the provided helpers to filter the spans and retrieve relevant information
for a more detailed inspection of the trace:

```python
from any_agent.tracing.attributes import GenAI

for span in agent_trace.spans:
    if span.is_tool_execution():
        tool_name = span.attributes.get(GenAI.TOOL_NAME)
        tool_args = span.attributes.get(GenAI.TOOL_ARGS)
        print(
            f"{tool_name}: {tool_args}"
        )
```
