from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import socket
import sys
import time
import random

producer_conf = {'bootstrap.servers': '127.0.0.1:9092',
        'client.id': socket.gethostname()}

admin_client = AdminClient({"bootstrap.servers":"127.0.0.1:9092"})

producer = Producer(producer_conf)

# create topic
topic_list = []
topic_list.append(NewTopic("credit_card", 1, 1))
admin_client.create_topics(topic_list)


def read_csv_and_send(producer,topic):

        #send data
        try:
        # send row by row
            for i in range(100):
                    producer.produce(topic, value=str(i))
                    producer.poll(1000)  
                    print(f"Đã gửi dữ liệu {i} tới topic '{topic}'")    
                    random_sleep_time = random.uniform(1, 1)
                    time.sleep(random_sleep_time)

            producer.flush()

            print(f"Dữ liệu đã được gửi tới topic '{topic}' thành công.")
        except Exception as e:
                print(f"Lỗi khi gửi dữ liệu tới topic '{topic}': {str(e)}")
        finally:
                producer.close()


if __name__ == "__main__":
        topic = "credit_card"
        read_csv_and_send(producer,topic)
        