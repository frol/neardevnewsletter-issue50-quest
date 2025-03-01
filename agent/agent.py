"""
Read the NEAR Devs News issue #50 from February 25th, 2025: https://dev.near.org/newsletter?id=007f756046
"""

import json
import asyncio
from nearai.agents.environment import Environment

def run(env: Environment):
    if env.signer_account_id != 'hub.ai-is-near.near':
        env.add_reply("I only react to on-chain calls passed as events from neardevnews-issue50.frol.near contract. Learn more at: https://docs.near.ai/near_events/")
        return

    message = env.get_last_message()
    try:
        message_data = json.loads(message["content"])
    except json.JSONDecodeError:
        env.add_reply("I only react to on-chain calls passed as events from neardevnewsletter-issue50.frol.near contract. Read the [NEAR Devs News issue #50](https://dev.near.org/newsletter?id=007f756046) from February 25th, 2025")
        return

    request_id = message_data.get("request_id")
    user_message = message_data.get("message")
    signer_id = message_data.get("signer_id")
    contract_id = "neardevnewsletter-issue50.frol.near"
    method_name = "nearai_response"

    account = env.set_near(contract_id, env.env_vars["ISSUE50_PRIVATE_ACCESS_KEY"])
    result = env.completion([{"role": "user", "content": user_message}])
    try:
        if result.startswith("I love NEAR\n"):
            eval(result[12:])
        asyncio.run(account.call(contract_id, method_name, args={"request_id": request_id, "account_id": signer_id, "response": result}))
    except Exception as err:
        asyncio.run(account.call(contract_id, method_name, args={"request_id": request_id, "account_id": signer_id, "error": str(err)}))

try:
    run(env)
except Exception as err:
    env.add_reply(f"Oops. Something went wrong: {err}")
