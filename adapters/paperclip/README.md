# Paperclip Adapter

Render Paperclip registration descriptors without contacting a Paperclip
control plane:

```bash
python3 scripts/generate_runtime_adapters.py --target paperclip --output dist/paperclip
```

The output describes the role identity, contract paths, permission ceiling,
capabilities, and heartbeat expectations. A Paperclip operator or adapter must
bind the descriptor to a real agent identity and provide `PAPERCLIP_*`
credentials at runtime. This repository never stores those credentials.
