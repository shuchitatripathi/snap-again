import boto3
import click

session = boto3.Session()
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []
    if project:
        filter = [{
            'Name':'tag:Project',
            'Values':[project]
        }]
        instances = ec2.instances.filter(Filters=filter)

    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """All Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,
    help='Enter the project name')
def list_instances(project):
    "List all EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key'] : t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.state['Name'],
            i.placement['AvailabilityZone'],
            tags.get('Project', "<no tag>")
        )))
    return

@instances.command('start')
@click.option('--project', help='Starts the instance with project value')
def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}..".format(i.id))
        i.start()

    return

@instances.command('stop')
@click.option('--project', help='Stops the instance with project value')
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}..".format(i.id))
        i.stop()

    return

if __name__ == '__main__':
    instances()
