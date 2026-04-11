import boto3
from botocore.exceptions import ClientError

def cleanup_orphaned_volumes():
    # Initialize the EC2 resource
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    
    # 1. Filter for 'available' volumes (those not attached to an EC2 instance)
    volumes = ec2.volumes.filter(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )

    for volume in volumes:
        v_id = volume.id
        
        # 2. Safety Check: Skip if the volume has a 'Keep' tag
        tags = {tag['Key']: tag['Value'] for tag in (volume.tags or [])}
        if tags.get('Keep') == 'true':
            print(f"Skipping Volume {v_id} - Protection tag found.")
            continue

        try:
            print(f"Processing Volume: {v_id}")

            # 3. Create a final snapshot before deletion (Compliance)
            snapshot = volume.create_snapshot(Description=f"Final backup before cleanup of {v_id}")
            
            # 4. Use a Waiter to ensure the snapshot is complete before deleting the volume
            snapshot.wait_until_completed()
            print(f"Snapshot {snapshot.id} completed.")

            # 5. Delete the orphaned volume
            volume.delete()
            print(f"Successfully deleted volume {v_id}.")

        except ClientError as e:
            print(f"Error processing {v_id}: {e}")

if __name__ == "__main__":
    cleanup_orphaned_volumes()