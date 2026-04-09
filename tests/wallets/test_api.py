import pytest
import json
from fastapi import status

@pytest.mark.asyncio
async def test_wallet_full_lifecycle(client):
    print("\n🚀 STARTING WALLET MODULE INTEGRATION TESTS")

    # --- 1. CREATE (SINGLE) ---
    print("\n--- 1. Single Wallet Creation ---")
    # Payload matches WalletCreate schema
    new_wallet_data = {
        "name": "Main Savings", 
        "type": "SAVINGS", 
        "balance": 1000.50
    }
    res = await client.post("/wallets/", json=new_wallet_data)
    
    print(f"Status Received: {res.status_code}")
    print(f"Response Body: {json.dumps(res.json(), indent=2, ensure_ascii=False)}")
    
    assert res.status_code == status.HTTP_201_CREATED
    wallet_id = res.json()["id"]
    assert res.json()["name"] == "Main Savings"

    # --- 2. BULK CREATE ---
    print("\n--- 2. Bulk Wallet Creation ---")
    # Wrapped in 'wallets' key as per WalletsCreate schema
    bulk_data = {
        "wallets": [
            {"name": "Emergency Fund", "type": "SAVINGS", "balance": 5000},
            {"name": "Daily Expenses", "type": "SPENDINGS", "balance": 0}
        ]
    }
    res = await client.post("/wallets/bulk", json=bulk_data)
    
    print(f"Status Received: {res.status_code}")
    assert res.status_code == status.HTTP_201_CREATED
    created_bulk = res.json()
    print(f"Items Created: {len(created_bulk)}")
    bulk_ids = [w["id"] for w in created_bulk]

    # --- 3. READ (FILTERING) ---
    print("\n--- 3. Filtering Test (Types: SAVINGS) ---")
    # Testing WalletFilters schema via query parameters
    res = await client.get("/wallets/", params={"types": ["SAVINGS"]})
    
    print(f"Savings Wallets Found: {len(res.json())}")
    assert res.status_code == status.HTTP_200_OK
    assert all(w["type"] == "SAVINGS" for w in res.json())

    # --- 4. BULK UPDATE (PATCH) ---
    print("\n--- 4. Bulk Update Test ---")
    # Updating one name and one balance using WalletsUpdate schema
    update_data = {
        "wallets": [
            {"id": bulk_ids[0], "name": "Super Emergency Fund"},
            {"id": bulk_ids[1], "balance": 250.75}
        ]
    }
    res = await client.patch("/wallets/bulk", json=update_data)
    
    print(f"Status Received: {res.status_code}")
    assert res.status_code == status.HTTP_200_OK
    updated_res = res.json()
    assert updated_res[0]["name"] == "Super Emergency Fund"
    # Convert Decimal string from JSON to float for comparison
    assert float(updated_res[1]["balance"]) == 250.75

    # --- 5. PARTIAL CONTENT TEST (207 Multi-Status) ---
    print("\n--- 5. Partial Success Test (One valid ID, one invalid) ---")
    partial_update = {
        "wallets": [
            {"id": wallet_id, "name": "Renamed Main"},
            {"id": 999999, "name": "Ghost Wallet"} # Non-existent ID
        ]
    }
    res = await client.patch("/wallets/bulk", json=partial_update)
    
    print(f"Status Received (Expected 207): {res.status_code}")
    print(f"Successfully Updated Objects: {len(res.json())}")
    # Verifying our custom logic for partial updates
    assert res.status_code == status.HTTP_207_MULTI_STATUS
    assert len(res.json()) == 1 

    # --- 6. DELETE (SINGLE) ---
    print("\n--- 6. Single Wallet Deletion ---")
    res = await client.delete(f"/wallets/{wallet_id}")
    print(f"Status Received: {res.status_code}")
    # Standard for successful deletion with no return body
    assert res.status_code == status.HTTP_204_NO_CONTENT

    # --- 7. BULK DELETE ---
    print("\n--- 7. Bulk Deletion Test ---")
    delete_payload = {"ids": bulk_ids}
    res = await client.request("DELETE", "/wallets/bulk", json=delete_payload)
    
    print(f"Status Received: {res.status_code}")
    print(f"Deleted IDs List: {res.json()}")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 2

    # --- 8. FINAL VERIFICATION ---
    print("\n--- 8. Final Cleanup Check ---")
    # Verifying that deleted IDs are truly gone
    check_res = await client.get(f"/wallets/{bulk_ids[0]}")
    assert check_res.status_code == status.HTTP_404_NOT_FOUND
    
    print("\n✅ ALL WALLET LIFECYCLE TESTS PASSED")