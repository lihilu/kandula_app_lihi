import os

import boto3
import pytest
from moto import mock_ec2

import datetime

from app.src.services.instance_data import InstanceData
from app.tests.utils.ec2_instances_builder import EC2InstancesBuilderForTests


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    yield aws_credentials


@pytest.fixture
def fake_ec2_client(aws_credentials):
    with mock_ec2():
        client = boto3.client('ec2')
        yield client


# noinspection PyUnusedLocal
def test_should_get_instance_list_when_no_instances_found(fake_ec2_client):
    instances = InstanceData(fake_ec2_client).get_instances()
    assert instances == {'Instances': []}


def test_should_get_single_instance_when_found(fake_ec2_client):
    expected_instance, = EC2InstancesBuilderForTests(fake_ec2_client).build()
    instances_result = InstanceData(fake_ec2_client).get_instances()

    assert instances_result == {
        'Instances': [
            {
                'Cloud': 'aws',
                'Region': 'us-east-1',
                'Id': expected_instance['InstanceId'],
                'Type': expected_instance['InstanceType'],
                'ImageId': expected_instance['ImageId'],
                'LaunchTime': expected_instance['LaunchTime'],
                'State': expected_instance['State']['Name'],
                'StateReason': None,
                'SubnetId': expected_instance['SubnetId'],
                'VpcId': expected_instance['VpcId'],
                'MacAddress': expected_instance["NetworkInterfaces"][0]['MacAddress'],
                'NetworkInterfaceId': expected_instance["NetworkInterfaces"][0]['NetworkInterfaceId'],
                'PrivateDnsName': expected_instance['PrivateDnsName'],
                'PrivateIpAddress': expected_instance['PrivateIpAddress'],
                'PublicDnsName': expected_instance['PublicDnsName'],
                'PublicIpAddress': expected_instance['PublicIpAddress'],
                'RootDeviceName': expected_instance['RootDeviceName'],
                'RootDeviceType': expected_instance['RootDeviceType'],
                'SecurityGroups': expected_instance['SecurityGroups'],
                'Tags': [{'Key': 'Name', 'Value': get_expected_name_from_tags(expected_instance)}],
            }
        ]
    }


def test_should_get_multiple_instances_in_different_state(fake_ec2_client):
    first_expected_instance, = EC2InstancesBuilderForTests(fake_ec2_client).build()
    second_expected_instance, = EC2InstancesBuilderForTests(fake_ec2_client).with_type('m4.large').stopped().build()
    instances_result = InstanceData(fake_ec2_client).get_instances()

    assert instances_result == {
        'Instances': [
            {
                'Cloud': 'aws',
                'Region': 'us-east-1',
                'Id': first_expected_instance['InstanceId'],
                'Type': first_expected_instance['InstanceType'],
                'ImageId': first_expected_instance['ImageId'],
                'LaunchTime': first_expected_instance['LaunchTime'],
                'State': first_expected_instance['State']['Name'],
                'StateReason': None,
                'SubnetId': first_expected_instance['SubnetId'],
                'VpcId': first_expected_instance['VpcId'],
                'MacAddress': first_expected_instance["NetworkInterfaces"][0]['MacAddress'],
                'NetworkInterfaceId': first_expected_instance["NetworkInterfaces"][0]['NetworkInterfaceId'],
                'PrivateDnsName': first_expected_instance['PrivateDnsName'],
                'PrivateIpAddress': first_expected_instance['PrivateIpAddress'],
                'PublicDnsName': first_expected_instance['PublicDnsName'],
                'PublicIpAddress': first_expected_instance['PublicIpAddress'],
                'RootDeviceName': first_expected_instance['RootDeviceName'],
                'RootDeviceType': first_expected_instance['RootDeviceType'],
                'SecurityGroups': first_expected_instance['SecurityGroups'],
                'Tags': [{'Key': 'Name', 'Value': get_expected_name_from_tags(first_expected_instance)}],
            },
            {
                'Cloud': 'aws',
                'Region': 'us-east-1',
                'Id': second_expected_instance['InstanceId'],
                'Type': second_expected_instance['InstanceType'],
                'ImageId': second_expected_instance['ImageId'],
                'LaunchTime': second_expected_instance['LaunchTime'],
                'State': second_expected_instance['State']['Name'],
                'StateReason': second_expected_instance['StateReason']['Message'],
                'SubnetId': second_expected_instance['SubnetId'],
                'VpcId': second_expected_instance['VpcId'],
                'MacAddress': second_expected_instance["NetworkInterfaces"][0]['MacAddress'],
                'NetworkInterfaceId': second_expected_instance["NetworkInterfaces"][0]['NetworkInterfaceId'],
                'PrivateDnsName': second_expected_instance['PrivateDnsName'],
                'PrivateIpAddress': second_expected_instance['PrivateIpAddress'],
                'PublicDnsName': second_expected_instance['PublicDnsName'],
                'PublicIpAddress': None,
                'RootDeviceName': second_expected_instance['RootDeviceName'],
                'RootDeviceType': second_expected_instance['RootDeviceType'],
                'SecurityGroups': second_expected_instance['SecurityGroups'],
                'Tags': [{'Key': 'Name', 'Value': get_expected_name_from_tags(second_expected_instance)}],
            }
        ]
    }


def get_expected_name_from_tags(instance):
    return next(iter([tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name']))
