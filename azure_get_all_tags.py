import csv
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient

# Initialize Azure credentials
credential = DefaultAzureCredential()

# Initialize the Subscription client
subscription_client = SubscriptionClient(credential)

def fetch_resource_groups(subscription_id):
    resource_groups = []
    
    resource_client = ResourceManagementClient(credential, subscription_id)
    for group in resource_client.resource_groups.list():
        resource_groups.append({
            "Subscription": subscription_id,
            "Resource Group": group.name,
            "Tags": group.tags
        })
    
    return resource_groups

def save_to_csv(data):
    with open("resource_groups_tags.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Subscription", "Resource Group", "Tags"])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    for subscription in subscription_client.subscriptions.list():
        subscription_id = subscription.subscription_id
        print(f"Fetching data for subscription: {subscription.display_name}")
        
        resource_groups_data = fetch_resource_groups(subscription_id)
        save_to_csv(resource_groups_data)
        
    print("Data saved to resource_groups_tags.csv")
