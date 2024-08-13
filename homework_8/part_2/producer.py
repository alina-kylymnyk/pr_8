import pika
import json
from faker import Faker
from models import Contact

fake = Faker()

rabbitmq_host = 'localhost'
queue_name = 'email_queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue=queue_name)

def generate_fake_contacts(num_contacts):
    for _ in range(num_contacts):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            additional_info=fake.text()
        )
        contact.save()
        message = {'contact_id': str(contact.id)}
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message)
        )
        print(f"Sent message for contact ID: {contact.id}")

if __name__ == "__main__":
    generate_fake_contacts(10)  
    connection.close()
