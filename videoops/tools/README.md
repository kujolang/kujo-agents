# VideoOps production tools

Canonical executable tooling for the VideoOps agents in this repository. No `kujo-videoops` checkout, legacy fixture runner, job API, or private account is required for local verification. The Producer and five specialists remain in `videoops/`; these tools implement their bounded media and review operations.

Run from any directory:

```sh
/absolute/kujo-agents/videoops/tools/bin/videoops media doctor --workspace /absolute/production
/absolute/kujo-agents/videoops/tools/bin/videoops media generate --workspace /absolute/production --request /absolute/production/requests/narration.json
/absolute/kujo-agents/videoops/tools/bin/videoops review status --workspace /absolute/production
python3 /absolute/kujo-agents/videoops/tools/scripts/qa_media.py /absolute/production --audio-only --video assets/voice.wav
```

Requirements: POSIX macOS/Linux, Python >=3.10, jsonschema >=4.18,<5, FFmpeg and ffprobe. Install with `python3 -m pip install /absolute/kujo-agents/videoops/tools` in a dedicated virtual environment. Distribution name is `kujo-agents-videoops`; Python imports and the `videoops` CLI retain compatibility. Do not co-install the retired `kujo-videoops` distribution in that environment because both provide the same module namespace. Existing workspace contracts, secret references and ledgers remain unchanged.

The canonical contracts live in `contracts/`. `scripts/build_media_contracts.py` generates media schemas; `scripts/sync_package_schemas.py` packages them. The repository's native `scripts/sync_videoops_media_contracts.kujo` synchronizes portable role copies locally. No sibling runtime supplies contracts.

```sh
bash videoops/tools/tests/run.sh # from kujo-agents root
```

The retained provider, audio QA and review regression tests run offline. The isolated-checkout test copies only this tool directory and proves generation/import/review CLI discovery without the retired repo. Automated tests never resolve a real secret or spend provider credits.

See [provider setup](docs/media-providers.md), [source-aware audio QA](docs/audio-qa.md), and [migration provenance](docs/migration-source.json). The historical live TTS receipt is preserved with its original verification date and source; it is not a new provider call. SFX access remains unverified after an unauthorized result, and Free-plan Music API generation remains blocked. No listening approval is inferred.
