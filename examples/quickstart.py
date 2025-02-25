from pluggy_py.client import PluggyClient

def main():
    # Instantiate the client with your credentials
    client = PluggyClient(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
    )

    # Authenticate to obtain the API key
    client.authenticate()

    if client.api_key:
        print("Successfully authenticated!")
        print("Your API key is:", client.api_key)
    else:
        print("Authentication failed. Please check your credentials.")

    # Retrieve an item ID from a local YAML file items.yaml (same directory as this script)
    yaml_items = client.items.retrieve_yaml_items()
    item_id = yaml_items[0]["id"]
    print(f"\nRetrieved item ID: {item_id} from items.yaml")

    # Fetch all accounts with internal paging
    try:
        all_accounts = client.accounts.list_all_accounts(item_id=item_id)
        print(f"\nFound total {len(all_accounts)} accounts across all pages for item: {item_id}")
        for acc in all_accounts:
            print(f"  ID: {acc.id}, Type: {acc.type}, Name: {acc.name}, Balance: {acc.balance}")
    except Exception as e:
        print(f"Error listing all accounts: {e}")

    # Fetch all transactions with internal paging
    try:
        all_transactions = client.transactions.list_all_transactions(account_id="ACCOUNT_ID")
        print(f"\nFound total {len(all_transactions)} transactions across all pages for account: 1")
        for tx in all_transactions:
            print(f"  ID: {tx.id}, Amount: {tx.amount}, Date: {tx.date}, Description: {tx.description}")
    except Exception as e:
        print(f"Error listing all transactions: {e}")

    # Fetch all investments with internal paging
    try:
        all_investments = client.investments.list_all_investments(item_id=item_id)
        print(f"\nFound total {len(all_investments)} investments across all pages for item: {item_id}")
        for inv in all_investments:
            print(f"  ID: {inv.id}, Name: {inv.name}, Value: {inv.value}")
    except Exception as e:
        print(f"Error listing all investments: {e}")

    # Fetch all bils with internal paging
    try:
        all_bills = client.bills.list_all_bills(account_id="ACCOUNT_ID")
        print(f"\nFound total {len(all_bills)} bills across all pages")
        for bill in all_bills:
            print(f"Account ID: {bill.id}, dueDate: {bill.dueDate}, Amount: {bill.totalAmount}")
    except Exception as e:
        print(f"Error listing all bills: {e}")


if __name__ == "__main__":
    main()
