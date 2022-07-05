from boto3 import client

def get_state_reason(instance):
    instance_state = instance['State']['Name']
    if instance_state != 'running':
        return instance['StateReason']['Message']


class InstanceData:
    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def check_value(self, instance, key):
        return instance.get(key)

    def get_instances(self):
        response = self.ec2_client.describe_instances()
        region= self.ec2_client.meta.region_name
        response_list = response['Reservations']
        my_instances = {'Instances':[]}
        for each_response in response_list:
            instance = each_response['Instances'][0]
            single_instance={}
            single_instance['Cloud'] = 'aws'
            single_instance['Region'] = region
            single_instance['Id'] = self.check_value(instance,'InstanceId')
            single_instance['Type'] = self.check_value(instance,'InstanceType')
            single_instance['ImageId'] = self.check_value(instance,'ImageId')
            single_instance['LaunchTime'] = self.check_value(instance,'LaunchTime')
            single_instance['State'] = self.check_value(instance['State'],'Name')
            if instance['State']['Name'] == 'running':
                single_instance['StateReason'] = 'None'
            else:
                single_instance['StateReason'] = self.check_value(instance['StateReason'],'Message')
            single_instance['SubnetId'] = self.check_value(instance,'SubnetId')
            single_instance['VpcId'] = self.check_value(instance,'VpcId')
            if len(instance['NetworkInterfaces'])==0:
                single_instance['MacAddress'] = ""
                single_instance['NetworkInterfaceId'] = ""
            else:
                single_instance['MacAddress'] = instance['NetworkInterfaces'][0]['MacAddress']
                single_instance['NetworkInterfaceId'] = instance['NetworkInterfaces'][0]['NetworkInterfaceId']
            single_instance['PrivateIpAddress'] = self.check_value(instance,'PrivateIpAddress')
            single_instance['PrivateDnsName'] = self.check_value(instance,'PrivateDnsName')
            single_instance['PublicDnsName'] = self.check_value(instance,'PublicDnsName')
            single_instance['PublicIpAddress'] = self.check_value(instance,'PublicIpAddress')
            single_instance['RootDeviceName'] = self.check_value(instance,'RootDeviceName')
            single_instance['RootDeviceType'] = self.check_value(instance,'RootDeviceType')
            single_instance['SecurityGroups'] = self.check_value(instance,'SecurityGroups')
            single_instance['Tags'] = self.check_value(instance,'Tags')

            my_instances['Instances'].append(single_instance)

        return my_instances


    def get_instances_list(self):
        response = self.ec2_client.describe_instances()
        region= self.ec2_client.meta.region_name
        response_list = response['Reservations']
        my_instances = {'Instances':[]}
        for each_response in response_list:
            instance = each_response['Instances'][0]
            single_instance={}
            single_instance['Id'] = self.check_value(instance,'InstanceId')
            single_instance['Type'] = self.check_value(instance,'InstanceType')
            single_instance['Region'] = region
            single_instance['State'] = self.check_value(instance['State'],'Name')
            if instance['State']['Name'] == 'running':
                single_instance['StateReason'] = 'None'
            else:
                single_instance['StateReason'] = self.check_value(instance['StateReason'],'Message')
            single_instance['PrivateIpAddress'] = self.check_value(instance,'PrivateIpAddress')
            my_instances['Instances'].append(single_instance)

        return my_instances
