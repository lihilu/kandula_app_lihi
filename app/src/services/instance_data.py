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

    def check_value(self, instance_to_check):
        result = ""
        #print (instance_to_check)
        try:
            instance_to_check != 'None'
            result = instance_to_check
            #print (result)
        except:
            result = "None"
        finally:
            return result

    def get_instances(self):
        response = self.ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['pending','running','shutting-down','stopped','stopping']}])
        region= self.ec2_client.meta.region_name
        response_list = response['Reservations']
        my_instances = {'Instances':[]}
        for each_response in response_list:
            instance = each_response['Instances'][0]
            single_instance={}
            single_instance['Cloud'] = 'aws'
            single_instance['Region'] = region
            single_instance['Id'] = self.check_value(instance['InstanceId'])
            single_instance['Type'] = self.check_value(instance['InstanceType'])
            single_instance['ImageId'] = self.check_value(instance['ImageId'])
            single_instance['LaunchTime'] = self.check_value(instance['LaunchTime'])
            single_instance['State'] = self.check_value(instance['State']['Name'])
            if instance['State']['Name'] == 'running':
                single_instance['StateReason'] = 'None'
            else:
                single_instance['StateReason'] = self.check_value(instance['StateReason']['Message'])
            single_instance['SubnetId'] = self.check_value(instance['SubnetId'])
            single_instance['VpcId'] = self.check_value(instance['VpcId'])
            single_instance['MacAddress'] = self.check_value(instance['NetworkInterfaces'][0]['MacAddress'])
            single_instance['NetworkInterfaceId'] = self.check_value(instance['NetworkInterfaces'][0]['NetworkInterfaceId'])
            single_instance['PrivateIpAddress'] = self.check_value(instance['PrivateIpAddress'])
            single_instance['PublicDnsName'] = self.check_value(instance['PublicDnsName'])
            single_instance['PublicIpAddress'] = self.check_value(instance['PublicIpAddress'])
            single_instance['RootDeviceName'] = self.check_value(instance['RootDeviceName'])
            single_instance['RootDeviceType'] = self.check_value(instance['RootDeviceType'])
            single_instance['SecurityGroups'] = self.check_value(instance['SecurityGroups'])
            single_instance['Tags'] = self.check_value(instance['Tags'])

            my_instances['Instances'].append(single_instance)

        return my_instances