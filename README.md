# CDP Agent Python Examples

Small Python examples for testing Coinbase CDP-style agent payment flows: creating charges, generating pay links, and checking wallet balances from an agent wrapper.

## Files

- `test-payments.py` — async smoke test for payment-related tools exposed by a `CDPAgent` implementation.

## Expected local setup

This repo is intentionally minimal and expects the actual agent implementation to be available in your Python path:

- `cdp_agent.py`
- `cdp_api_key.json`
- `wallet_data.txt`
- `.env` for local configuration

Those files may include credentials or local wallet state and should not be committed.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install python-dotenv
python test-payments.py
```

If your `CDPAgent` module has additional dependencies, install those before running the smoke test.

## Safety

Use test credentials and tiny amounts when experimenting. Payment links and wallet operations can create real on-chain or payment-provider actions depending on how your `CDPAgent` is configured.

## Related links

- [MeetKai](https://meetkai.xyz) — the operator layer behind Kai CMO workflows.
- [KaiCalls](https://kaicalls.com) — AI voice agents for small-business phone answering and lead capture.
- [Connor Gallic](https://connorgallic.com) — founder building Kai, KaiCalls, and AI automation systems.
