import logging
import time

import boto3 as boto3
from botocore.config import Config
from botocore.exceptions import ClientError


class AwsEC2Service:

    def __init__(self) -> None:
        self.ec2_resource = boto3.resource('ec2')
        self.ec2_client = boto3.client('ec2')

    def list_regions(self):
        results = []
        try:
            response = self.ec2_client.describe_regions()

            for resp in response['Regions']:
                region_name = resp['RegionName']
                end_point = resp['Endpoint']
                results.append({'region_name': region_name, 'end_point': end_point})
        except ClientError as e:
            logging.error(e)
            raise e
        return results

    def get_all_instances(self, region_name):
        results = []
        try:
            if region_name == 'all':
                for item in self.ec2_resource.instances.all():
                    results.append({
                        'id': item.id,
                        'name': item.key_name,
                        'ami': item.image_id,
                        'state': item.state['Name'],
                        'private_ip_address': item.private_ip_address,
                        'public_ip_address': item.public_ip_address,
                        'security_groups': item.security_groups,
                        'subnet_id': item.subnet_id,
                        'vpc_id': item.vpc_id
                    })
            else:
                ec2_resource_with_region = boto3.resource('ec2', region_name=region_name)
                for instance in ec2_resource_with_region.instances.all():
                    results.append({
                        'id': instance.id,
                        'name': instance.key_name,
                        'ami': instance.image_id,
                        'state': instance.state['Name'],
                        'private_ip_address': instance.private_ip_address,
                        'public_ip_address': instance.public_ip_address,
                        'security_groups': instance.security_groups,
                        'subnet_id': instance.subnet_id,
                        'vpc_id': instance.vpc_id
                    })
        except ClientError as e:
            logging.error(e)
            raise e
        return results
