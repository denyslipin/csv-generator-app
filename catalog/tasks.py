import os
import csv
import uuid
import boto3
from faker import Faker
from celery import shared_task

from django.utils.text import slugify
from app.settings import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
)

from catalog.models import Schema, Dataset


@shared_task
def generate_csv(rows, schema_id, dataset_id):
    schema = Schema.objects.get(id=schema_id)
    dataset = Dataset.objects.get(id=dataset_id)
    filename = f"{slugify(schema.name)}-{uuid.uuid4()}.csv"
    all_columns = schema.get_all_columns()
    first_row = [column.name for column in all_columns]
    fake_row_types = [column.type.name for column in all_columns]
    delimiter = schema.separator.name
    fake = Faker('en_US')
    with open(filename, "w") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=delimiter, lineterminator='\n'
        )
        writer.writerow(first_row)
        for _ in range(rows):
            gen_fake = {
                "email": fake.email(),
                "name": fake.name(),
                'job': fake.job(),
                'company': fake.company(),
                "phone": fake.phone_number(),
                "address": fake.address(),
                "city": fake.city(),
                "country": fake.country(),
            }
            fake_row = []
            for column_type in fake_row_types:
                if column_type in gen_fake:
                    fake_row.append(gen_fake[column_type])
            writer.writerow(fake_row)

    dataset.csv_file = 'media/' + filename
    dataset.status = "Ready"
    dataset.save()

    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    s3.upload_file(
        filename, AWS_STORAGE_BUCKET_NAME, '%s/%s' % ('media', filename)
    )
    os.remove(filename)
