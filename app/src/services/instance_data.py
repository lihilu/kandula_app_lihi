from boto3 import client

SAMPLE_INSTANCE_DATA = {
    'Instances': [
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-53d13a927070628de', 'Type': 'a1.2xlarge',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-13T19:27:52.000Z', 'State': 'running',
         'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Jenkins Master'}]
         },
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-23a13a927070342ee', 'Type': 't2.medium',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Stopped',
         'StateReason': 'Client.UserInitiatedShutdown: User initiated shutdown', 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Consul Node'}]
         },
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-77z13a9270708asd', 'Type': 't2.xlarge',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Running',
         'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Grafana'}]
         }
    ]
}


def get_state_reason(instance):
    instance_state = instance['State']['Name']
    if instance_state != 'running':
        return instance['StateReason']['Message']


class InstanceData:
    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def get_instances(self):
        # TODO: The below JSON should be populated using real instance data (instead of the SAMPLE_INSTANCE_DATA)
        #       The format of SAMPLE_INSTANCE_DATA (field names and JSON structure)
        #       must be kept in order to be properly displayed in the application UI
        #
        #       Notice that when the machine is running the "StateReason" filed should be set to None
        #       and will not be shown in the UI
        #
        #       NOTE: the `self.ec2_client` is an object that is returned from doing `boto3.client('ec2')` as you can
        #       probably find in many examples on the web
        #       To read more on how to use Boto for EC2 look for the original Boto documentation
        try:
            response = self.ec2_client.describe_instances()
        except Exception as e:
            print (e)
        response_list = response['Reservations']
        my_instances = {'Instances':[]}
        for each_response in response_list:
            instance = each_response['Instances'][0]
            single_instance={}
            single_instance['Cloud'] = 'aws'
            single_instance['Region'] = response.meta.region_name
            single_instance['Id'] = instance['InstanceId']
            single_instance['Type'] = instance['InstanceType']
            single_instance['ImageId'] = instance['ImageId']
            single_instance['LaunchTime'] = instance['LaunchTime']
            single_instance['State'] = instance['State']['Name']
            if instance['State']['Name'] == 'running':
                single_instance['StateReason'] = 'None'
            else:
                single_instance['StateReason'] = instance['StateReason']['Message']
            if single_instance['SubnetId']:
                single_instance['SubnetId'] = instance['SubnetId']
            else:
                single_instance['SubnetId'] = 'None'
            if single_instance['VpcId']:
                single_instance['SubnetId'] = instance['VpcId']
            else:
                single_instance['VpcId'] = 'None' 
            if single_instance['NetworkInterfaceId']:
                single_instance['MacAddress'] = instance['NetworkInterfaces'][0]['MacAddress']
                single_instance['NetworkInterfaceId'] = instance['NetworkInterfaces'][0]['NetworkInterfaceId']
            else:
                single_instance['MacAddress'] ='None'
                single_instance['NetworkInterfaceId'] = 'None'
            single_instance['PrivateDnsName'] = instance['PrivateDnsName']
            try:
                single_instance['PrivateIpAddress'] = instance['PrivateIpAddress']
            except:
                single_instance['PrivateIpAddress'] = 'None'
            if single_instance['PublicDnsName']:
                single_instance['PublicDnsName'] = instance['PublicDnsName']
                single_instance['PublicIpAddress'] = instance['PublicIpAddress']
            else:
                single_instance['PublicDnsName'] = 'None'
                single_instance['PublicIpAddress'] = 'None'
            single_instance['RootDeviceName'] = instance['RootDeviceName']
            single_instance['RootDeviceType'] = instance['RootDeviceType']
            single_instance['SecurityGroups'] = instance['SecurityGroups']
            single_instance['Tags'] = instance['Tags']

            my_instances['Instances'].append(single_instance)

        return my_instances
        # return SAMPLE_INSTANCE_DATA