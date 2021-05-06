import boto3
from datetime import datetime, timedelta

from ptCryptoClub.admin.config import CloudWatchLogin


class UsageStats:
    # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/monitoring-cloudwatch.html
    def cpu_utilization_ec2(self, instance):
        client = boto3.client(
            "cloudwatch",
            aws_access_key_id=CloudWatchLogin().aws_access_key_id,
            aws_secret_access_key=CloudWatchLogin().aws_secret_access_key,
            region_name=CloudWatchLogin().region_name
        )
        response = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance
                },
            ],
            StartTime=datetime.utcnow().replace(minute=0, second=0) - timedelta(hours=24),
            EndTime=datetime.utcnow(),
            Period=600,  # in seconds
            Statistics=[
                'Average', 'Maximum', 'Minimum'
            ],
            Unit='Percent'
        )
        list_ = []
        aux = response['Datapoints']
        if len(aux) > 0:
            aux.sort(key=lambda item: item['Timestamp'], reverse=False)
        for i in aux:
            list_.append(
                {
                    'date': str(i['Timestamp'])[:19],
                    'avg': round(i['Average'], 2),
                    'max': round(i['Maximum'], 2),
                    'min': round(i['Minimum'], 2)
                }
            )
        return list_

    def cpu_utilization_db(self, instance):
        client = boto3.client(
            "cloudwatch",
            aws_access_key_id=CloudWatchLogin().aws_access_key_id,
            aws_secret_access_key=CloudWatchLogin().aws_secret_access_key,
            region_name=CloudWatchLogin().region_name
        )
        response = client.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                    'Name': 'DBInstanceIdentifier',
                    'Value': instance
                },
            ],
            StartTime=datetime.utcnow().replace(minute=0, second=0) - timedelta(hours=24),
            EndTime=datetime.utcnow(),
            Period=600,  # in seconds
            Statistics=[
                'Average', 'Maximum', 'Minimum'
            ],
            Unit='Percent'
        )
        list_ = []
        aux = response['Datapoints']
        if len(aux) > 0:
            aux.sort(key=lambda item: item['Timestamp'], reverse=False)
        for i in aux:
            list_.append(
                {
                    'date': str(i['Timestamp'])[:19],
                    'avg': round(i['Average'], 2),
                    'max': round(i['Maximum'], 2),
                    'min': round(i['Minimum'], 2)
                }
            )
        return list_

    def ram_utilization_db(self, instance):
        client = boto3.client(
            "cloudwatch",
            aws_access_key_id=CloudWatchLogin().aws_access_key_id,
            aws_secret_access_key=CloudWatchLogin().aws_secret_access_key,
            region_name=CloudWatchLogin().region_name
        )
        response = client.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='FreeableMemory',
            Dimensions=[
                {
                    'Name': 'DBInstanceIdentifier',
                    'Value': instance
                },
            ],
            StartTime=datetime.utcnow().replace(minute=0, second=0) - timedelta(hours=24),
            EndTime=datetime.utcnow(),
            Period=300,  # in seconds
            Statistics=[
                'Minimum'
            ],
            Unit='Bytes'
        )
        list_ = []
        aux = response['Datapoints']
        if len(aux) > 0:
            aux.sort(key=lambda item: item['Timestamp'], reverse=False)
        for i in aux:
            list_.append(
                {
                    'date': str(i['Timestamp'])[:19],
                    'min': round(i['Minimum'], -6)
                }
            )
        return list_

    def connections_db(self, instance):
        client = boto3.client(
            "cloudwatch",
            aws_access_key_id=CloudWatchLogin().aws_access_key_id,
            aws_secret_access_key=CloudWatchLogin().aws_secret_access_key,
            region_name=CloudWatchLogin().region_name
        )
        response = client.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='DatabaseConnections',
            Dimensions=[
                {
                    'Name': 'DBInstanceIdentifier',
                    'Value': instance
                },
            ],
            StartTime=datetime.utcnow().replace(minute=0, second=0) - timedelta(hours=24),
            EndTime=datetime.utcnow(),
            Period=300,  # in seconds
            Statistics=[
                'Maximum'
            ],
            Unit='Count'
        )
        list_ = []
        aux = response['Datapoints']
        if len(aux) > 0:
            aux.sort(key=lambda item: item['Timestamp'], reverse=False)
        for i in aux:
            list_.append(
                {
                    'date': str(i['Timestamp'])[:19],
                    'max': i['Maximum']
                }
            )
        return list_
