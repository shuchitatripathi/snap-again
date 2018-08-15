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
def cli():
    """Commands for instances, volumes and snapshots"""

@cli.group('snapshots')
def snapshots():
    "All commands for snapshots"

@snapshots.command('list')
@click.option('--project', default=None,
    help='Enter the project name')
@click.option('--all', 'list_all', default=False, is_flag=True,
    help = 'List all snapshots')
def list_snapshots(project, list_all):
    "List all snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
                if s.state == 'completed' and not list_all: break
    return

@cli.group('volumes')
def volumes():
    """All commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
    help='Enter the project name')
def list_volumes(project):
    "List all Instances' volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
            )))
    return

@cli.group('instances')
def instances():
    "All Commands for instances"

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
@click.option('--project', default=None,
    help='Enter the project name')
def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)

    try:
        for i in instances:
            print("Starting {0}..".format(i.id))
            i.start()
    except:
        print("Could not start {0}..".format(i.id))
    return

@instances.command('stop')
@click.option('--project', default=None,
    help='Enter the project name')
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    try:
        for i in instances:
            print("Stopping {0}..".format(i.id))
            i.stop()
    except:
        print("Could not stop {0}..".format(i.id))
    return

@instances.command('createsnap')
@click.option('--project', default=None,
    help='Enter the project name')
def create_snapshot(project):
    "Create snapshot"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print("Stopping {0}..".format(i.id))
            i.stop()
            i.wait_until_stopped()
            print("Creating snapshot of {0}..".format(v.id))
            v.create_snapshot(Description='created from cli')
            print("Starting {0}..".format(i.id))
            i.start()
            i.wait_until_running()
    print("Job's done!!")
    return

if __name__ == '__main__':
    cli()
