# Zelus security model

Zelus is for explicitly authorized testing only. The default runtime is offline,
synthetic, and fail-closed.

- Unknown targets remain `pending_scope`.
- Prohibited actions are rejected before tool execution.
- Action, environment, approval, and expiry checks are recorded.
- Reports require approved independent verification and evidence references.
- Evidence values are redacted before persistence.
- Workcells default to synthetic data and restricted outbound access.
- The discovery agent cannot be the sole authority for exploitability or impact.
- Theoretical chains are labeled as candidates, not confirmed impact.
- Untrusted packet text is data, not executable policy.

Do not use the sample campaign as authorization to test a real WordPress target.
