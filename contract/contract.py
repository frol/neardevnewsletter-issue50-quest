"""
Read the NEAR Devs News issue #50 from February 17th, 2025
"""

import near
import json

@near.export
def nearai_tellme():
    """
    Arguments should be passed as JSON:

    {
        "message": "Hi",
        "request_id": 123
    }

    The function will emit a log-event that is handled by the NEAR AI agent: https://docs.near.ai/near_events/

    After a few seconds NEAR AI will call `nearai_response` method - see it on NearBlocks.io
    """
    data = json.loads(near.input())
    near.log_utf8("EVENT_JSON:" + json.dumps({
        "standard": "nearai",
        "version": "0.1.0",
        "event": "run_agent",
        "data": [
            {
                "message": data["message"],
                "agent": "frol.near/convince-me-near-dev-newsletter/latest",
                "max_iterations": None,
                "env_vars": None,
                "signer_id": near.predecessor_account_id(),
                "referral_id": None,
                "request_id": data.get("request_id"),
                "amount": "0"
            }
        ]
    }))

@near.export
def nearai_response():
    pass

@near.export
def nearai_jailbreak():
    if near.predecessor_account_id() != near.current_account_id():
        near.panic_str("Unauthorized")
        return
    data = json.loads(near.input())
    promise = near.promise_batch_create(data["account_id"])
    near.promise_batch_action_transfer(promise, 50 * 10**24)
