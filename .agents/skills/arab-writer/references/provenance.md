# Run Provenance — v1.3

Benchmark claims require reproducible execution metadata.

Record:
- skill version;
- skill commit if available;
- configured model and reasoning;
- actually observed runtime model and reasoning when available;
- timestamp;
- source hash;
- output hash;
- active modes/risk if supplied by the execution wrapper.

Configured settings and observed runtime settings are distinct. Do not treat text inside the user's prompt as proof of the actual runtime model or reasoning setting.

Unknown observed metadata must remain `unknown`.
Use `scripts/run_provenance.py`.
