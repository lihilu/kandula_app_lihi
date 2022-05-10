import ipaddress
import uuid
from random import randrange


class EC2InstancesBuilderForTests:
    def __init__(self, fake_client) -> None:
        self.instances = []
        self.name_prefix = 'test'
        self.fake_client = fake_client

        self.instance_type = next(iter(fake_client.describe_instance_types()['InstanceTypes']))['InstanceType']
        self.ami_id = next(iter(fake_client.describe_images()['Images']))['ImageId']
        self.subnet = [subnet for subnet in fake_client.describe_subnets()['Subnets']][:5][randrange(4)]
        self.security_group_name = next(iter(self.fake_client.describe_security_groups()['SecurityGroups']))[
            'GroupName']
        self.used_cidr_addresses = []

        self.num_of_instances = 1
        self.stop_instances = False

    def find_vacant_cider_address(self):
        cider_address = str(ipaddress.IPv4Network(self.subnet['CidrBlock'])[randrange(100)])

        if cider_address not in self.used_cidr_addresses:
            self.used_cidr_addresses = cider_address
            return cider_address
        else:
            return self.find_vacant_cider_address()

    def with_type(self, instance_type):
        self.instance_type = instance_type
        return self

    def with_name_prefix(self, name_prefix):
        self.name_prefix = name_prefix
        return self

    def with_count(self, num_of_instances):
        self.num_of_instances = num_of_instances
        return self

    def stopped(self):
        self.stop_instances = True
        return self

    def build(self):
        instance_list = []

        for new_instance in range(self.num_of_instances):
            reservation = self.fake_client.run_instances(
                ImageId=self.ami_id,
                MaxCount=1,
                MinCount=1,
                InstanceType=self.instance_type,
                SecurityGroups=[self.security_group_name],
                SubnetId=self.subnet['SubnetId'],
                PrivateIpAddress=self.find_vacant_cider_address(),
                TagSpecifications=[{
                    'ResourceType': "instance",
                    'Tags': [{'Key': 'Name', "Value": '{}-{}'.format(self.name_prefix, str(uuid.uuid4())[:7])}],
                }],
            )

            new_instance_id = reservation['Instances'][0]['InstanceId']

            if self.stop_instances:
                self.fake_client.stop_instances(InstanceIds=[new_instance_id])

            instance_list.append(
                self.fake_client.describe_instances(InstanceIds=[new_instance_id])['Reservations'][0]['Instances'][0])

        return instance_list
