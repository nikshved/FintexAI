import json


def log(step: str, res):
    status = res.status_code
    symbol = "✅" if status < 400 else "❌"
    print(f"\n{'=' * 50}")
    print(f"{symbol}  {step}")
    print(f"{'=' * 50}")
    print(f"STATUS: {status}")
    try:
        print("BODY:")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception:
        print("BODY: (empty)")


async def test_wallet_crud(client):
    print("\n\n🚀 STARTING WALLET CRUD TEST")

    # CREATE
    res = await client.post("/wallets/", json={"name": "MyWallet", "type": "SAVINGS"})
    log("CREATE wallet", res)
    assert res.status_code == 201
    data = res.json()
    wallet_id = data["id"]
    assert data["balance"] == "0.00"
    assert data["name"] == "MyWallet"
    assert data["type"] == "SAVINGS"

    # READ
    res = await client.get(f"/wallets/{wallet_id}")
    log("READ wallet", res)
    assert res.status_code == 200
    assert res.json()["id"] == wallet_id

    # UPDATE
    res = await client.patch(f"/wallets/{wallet_id}", json={"name": "UpdatedWallet"})
    log("UPDATE wallet", res)
    assert res.status_code == 200
    assert res.json()["name"] == "UpdatedWallet"

    # DELETE
    res = await client.delete(f"/wallets/{wallet_id}")
    log("DELETE wallet", res)
    assert res.status_code == 204

    # VERIFY deleted
    res = await client.get(f"/wallets/{wallet_id}")
    log("VERIFY deleted", res)
    assert res.status_code == 404

    print("\n\n🎉 ALL STEPS PASSED\n")
