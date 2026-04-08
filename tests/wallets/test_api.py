import pytest
import json


@pytest.mark.asyncio
async def test_wallet_crud(client):
    # CREATE
    res = await client.post("/wallets/", json={"name": "Wallet", "balance": 100})

    print("STATUS:", res.status_code)
    print("BODY:")
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))

    assert res.status_code == 200
    data = res.json()
    wallet_id = data["id"]

    # READ
    res = await client.get(f"/wallets/{wallet_id}")
    assert res.status_code == 200

    # UPDATE
    res = await client.patch(f"/wallets/{wallet_id}", json={"balance": 500})
    assert res.json()["balance"] == 500

    # DELETE
    res = await client.delete(f"/wallets/{wallet_id}")
    assert res.status_code == 200

    # VERIFY
    res = await client.get(f"/wallets/{wallet_id}")
    assert res.status_code == 404
