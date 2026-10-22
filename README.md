# Skills by rittmang

Practical [Agent Skills](https://agentskills.io/) for reusable workflows. Each skill is a folder with a `SKILL.md` entry point and only the supporting files its workflow needs.

## Available skills

| Skill | What it does |
| --- | --- |
| [name-project](skills/name-project/SKILL.md) | Develop and compare project, product, or company names, with optional domain research. |
| [create-company-identity](skills/create-company-identity/SKILL.md) | Turn a company idea into positioning, a name, and a coherent domain/social identity with evidence for live checks. |

The company identity skill uses `name-project` when it is installed. Both work independently: the company skill has a naming fallback, and the project skill stays focused on naming and domains. Company identity covers brand setup, not incorporation or account creation.

## Install

Use the [skills CLI](https://github.com/vercel-labs/skills) with a current supported Node.js runtime:

```bash
# Inspect the available skills.
npx skills add rittmang/skills --list

# Install either skill.
npx skills add rittmang/skills --skill name-project
npx skills add rittmang/skills --skill create-company-identity

# Or install both for Codex.
npx skills add rittmang/skills --skill name-project --skill create-company-identity --agent codex
```

The CLI supports other agents as well. You can also copy an individual skill folder into your agent's documented skills location. The core instructions use the open Agent Skills format; `agents/openai.yaml` adds optional OpenAI UI metadata. Compatibility also depends on the tools available to the agent.

## Example requests

For naming only:

> Use name-project to name an open-source tool that turns bug reports into reproducible test cases. I want a short, memorable name with a calm engineering tone. Brainstorm only; skip domain research.

For naming with a domain constraint:

> Use name-project to explore names for a personal reading tracker. Compare the strongest options, then research exact-match .com and .app domains. My budget is $30 per year; don't assume I can buy an aftermarket name.

For a company identity:

> Use create-company-identity for a startup helping small architecture studios manage client approvals. Develop the positioning and name, then research a matching domain and Instagram and LinkedIn identifiers. Favor a consistent identity over a clever spelling.

For an existing name:

> Use create-company-identity to evaluate the name I've already chosen. Keep the name unless you find a strong reason to change it. Research a domain, a GitHub organization name, and an X handle, and distinguish confirmed findings from unresolved checks.

In Codex, you can explicitly invoke these as `$name-project` and `$create-company-identity`. In other agents, use their skill invocation mechanism or a natural-language request matching the skill description.

## Availability research

Ideation works without network access. Live domain, handle, and collision research needs browsing or lookup tools. No specific MCP server or paid service is required.

The naming skill includes an optional, standard-library-only RDAP helper requiring Python 3.10+:

```bash
python3 skills/name-project/scripts/check_domains.py example.com example.dev
```

It queries IANA-discovered registry services and emits timestamped JSON. It accepts ASCII second-level domains such as `example.com`; use registry or registrar tools for multi-label suffixes such as `example.co.uk` and raw Unicode names. Unsupported services and blocked requests stay `unknown`.

`not_found` is an RDAP result, not confirmation that a domain can be purchased. A registrar must confirm registrability and pricing. Likewise, an absent social profile does not prove a handle is claimable. The skills keep these evidence levels explicit and do not purchase domains or register accounts.

## Development and validation

Keep each skill focused. Put detailed, conditional guidance in linked `references/` files and repeatable mechanics in `scripts/`. Avoid machine-specific paths and undocumented tool dependencies.

Run the domain checker's offline behavior tests:

```bash
python3 -m unittest discover -s tests -v
```

The tests cover registered and not-found responses, malformed replies, rate limits, unsupported services, network failures, and input validation. They do not contact external services. For manual behavioral scenarios, see [evals/naming-scenarios.md](evals/naming-scenarios.md). Format validation alone does not establish naming quality or correct skill selection.

## Distribution

This GitHub repository is the canonical source. [skills.sh](https://skills.sh/docs/faq) lists skills through installation telemetry from the skills CLI. Other directories have their own indexing or contribution rules.

## License

[MIT](LICENSE).
