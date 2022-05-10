from boto3 import client


class InstanceActions:
    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def start_instance(self, instance_id):
        # TODO: Implement 'start instance' logic here using `self.ec2_client` as your boto client
        #       the `self.ec2_client` is an object that is returned from doing `boto3.client('ec2')` as you can
        #       probably find in many examples on the web
        #       To read more on how to use Boto for EC2 look for the original Boto documentation
        pass

    def stop_instance(self, instance_id):
        # TODO: Implement 'stop_instance' logic here using `self.ec2_client` as your boto client
        #       the `self.ec2_client` is an object that is returned from doing `boto3.client('ec2')` as you can
        #       probably find in many examples on the web
        #       To read more on how to use Boto for EC2 look for the original Boto documentation
        pass

    def terminate_instance(self, instance_id):
        # TODO: Implement 'terminate_instance' logic here using `self.ec2_client` as your boto client
        #       the `self.ec2_client` is an object that is returned from doing `boto3.client('ec2')` as you can
        #       probably find in many examples on the web
        #       To read more on how to use Boto for EC2 look for the original Boto documentation
        pass

    def action_selector(self, instance_action):
        return {
            'start': self.start_instance,
            'stop': self.stop_instance,
            'terminate': self.terminate_instance
        }.get(instance_action, lambda x: self.action_not_found(instance_action))

    @staticmethod
    def action_not_found(instance_action):
        raise RuntimeError("Unknown instance action selected: {}".format(instance_action))
