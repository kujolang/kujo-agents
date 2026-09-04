# VideoOps Permission Model

Permission is a run input and maximum bound; the Markdown package does not enforce it.

- `OBSERVE`: read inputs, inspect media, run non-mutating checks, and write review evidence.
- `PROPOSE`: includes OBSERVE and may write planning, sourcing, generation requests, fix lists, or proposed production artifacts.
- `ACT`: includes PROPOSE and only the explicitly authorized stage-local writes/renders. It never implies external publication, paid generation, account use, or arbitrary repository mutation.

The runtime adapter must constrain workspace roots, allowed tools, output paths, time/byte/process budgets, provider cost, and external effects. Credentials are supplied out of band and never stored in artifacts.
