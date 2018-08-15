import boto3
import click

session = boto3.Session()
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    "List all EC2 instances"
    for i in ec2.instances.all():
        print(', '.join((
            i.id,
            i.state['Name'],
            i.placement['AvailabilityZone']
        )))
    return

if __name__ == '__main__':
    list_instances()
