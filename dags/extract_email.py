import datetime
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from RPA.Browser.Selenium import Selenium
from RPA.Email.ImapSmtp import ImapSmtp
import os
from dotenv import load_dotenv
import datetime
import json
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from airflow.providers.apache.kafka.operators.consume import ConsumeFromTopicOperator
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import socket
import sys
import time
import random


mail = ImapSmtp(smtp_server=os.getenv("SMTP_SERVER"), smtp_port=os.getenv("SMTP_PORT"))
mail.authorize(account=os.getenv("GMAIL_ACCOUNT"), password=os.getenv("GMAIL_PASSWORD"))


def get_mails_content(criterion: str):
    mail = ImapSmtp(smtp_server=os.getenv("SMTP_SERVER"), smtp_port=os.getenv("SMTP_PORT"))
    mail.authorize(account=os.getenv("GMAIL_ACCOUNT"), password=os.getenv("GMAIL_PASSWORD"))
    
    mails = mail.list_messages(criterion=criterion)
    
    for m in mails:
        uid = m["uid"]
        sender = m["Message"].get("From")
        subject = m["Message"].get("Subject")
    
        attachment = mail.save_attachment(message=m["Message"], target_folder="/data/attachments/", overwrite=False)
        

def produce_to_kafka(topic: str):
    producer_conf = {'bootstrap.servers': 'kafka:19092'}
    admin_client = AdminClient({"bootstrap.servers":"kafka:19092"})                

    producer = Producer(producer_conf)
    
    topic_list = []
    topic_list.append(NewTopic(topic, 1, 1))
    admin_client.create_topics(topic_list)
    
    try:
        # send row by row
            for i in range(100):
                    producer.produce(topic, value=str(i))
                    producer.poll(1000)  
                    print(f"Đã gửi dữ liệu message {i} tới topic '{topic}'")    
                    random_sleep_time = random.uniform(1, 1)
                    time.sleep(random_sleep_time)

            producer.flush()

            print(f"Dữ liệu đã được gửi tới topic '{topic}' thành công.")
    except Exception as e:
        print(f"Lỗi khi gửi dữ liệu tới topic '{topic}': {str(e)}")

dag_id = os.path.basename(__file__).replace(".py", "")

with DAG(
    dag_id=dag_id,
    start_date=datetime.datetime(2024, 2, 21),
    schedule_interval='0 0 * * *',  # Chạy vào lúc 0 giờ mỗi ngày
    tags=["example"],
) as dag:
    get_mail = PythonOperator(
        task_id="get_mail",
        python_callable=get_mails_content,
        op_args=["gmail:'Message from RPA Python' after:15-12-2023"],
    )

    send_message = PythonOperator(
        task_id="send_message",
        python_callable=produce_to_kafka,
        op_args=["credit_card"],
    )

    get_mail >> send_message




