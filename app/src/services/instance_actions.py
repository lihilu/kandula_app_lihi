from boto3 import client


class InstanceActions:
    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def start_instance(self, instance_id):
        result=False
        try:
            responses = self.ec2_client.start_instances(InstanceIds=[instance_id])
            result= responses['ResponseMetadata']['HTTPStatusCode']== 200
       #     print (result)
        except Exception as e:
            print(e)
        finally:
            return result

    def stop_instance(self, instance_id):
        result= False
        try:
            responses = self.ec2_client.stop_instances(InstanceIds=[instance_id])
            result = responses['ResponseMetadata']['HTTPStatusCode']==200
        except Exception as e:
            print(e)
        return result

    def terminate_instance(self, instance_id):
        result= False
        try:
            responses = self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            result = responses['ResponseMetadata']['HTTPStatusCode']== 200
        except Exception as e:
            print(e)
        return result

    def action_selector(self, instance_action):
        return {
            'start': self.start_instance,
            'stop': self.stop_instance,
            'terminate': self.terminate_instance
        }.get(instance_action, lambda x: self.action_not_found(instance_action))

    @staticmethod
    def action_not_found(instance_action):
        raise RuntimeError("Unknown instance action selected: {}".format(instance_action))
