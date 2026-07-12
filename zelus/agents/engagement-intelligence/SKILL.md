---
name: engagement_packet_ingest
description: Parse and compile authorization, scope, policy, product, and target context.
version: 1
---

# Engagement intake skill

Compile the packet into `manifest.json`, validate required authorization fields,
preserve provenance, and create a missing-information register. Never treat a
public DNS record, product family, acquisition, or third-party integration as
authorization by itself.
