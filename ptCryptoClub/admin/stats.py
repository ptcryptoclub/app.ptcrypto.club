import boto3
from datetime import datetime, timedelta

from ptCryptoClub.admin.config import CloudWatchLogin


class UsageStats:
    def cpu_utilization(self, instance):
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
