# test-driven-agent-development

- :star: -> https://github.com/mozilla-ai/any-agent

## Setup

In order to follow the workshop, you need to make sure that you:

- Own a GitHub account.

### Pick your environment

| Recommended | For the adventurous  |
| -------------| ------------------- |
| [![Open on Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=1016187393&skip_quickstart=true) | [Local Setup](./docs/local-setup.md) |


### Prepare the credentials

In order to handle credentials, we recommend to create a file named `.env`.

```bash
touch .env
```

Inside it, you can paste the credentials needed for the agent to run:

- GEMINI_API_KEY: https://aistudio.google.com/apikey
- TAVILY_API_KEY: https://www.tavily.com/

## Workshop

1. [Python Workflow](./docs/1-python-workflow.md)

2. [Defining and Running Agents](./docs/2-defining-and-running-agents.md)

3. [Test Driven Agent Development](./docs/3-test-driven-agent-development.md)
