
import pika
import json
from models import Contact

rabbitmq_host = 'localhost'
queue_name = 'email_queue'

def simulate_email_sending(email):
    print(f"Sending email to: {email}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    
    contact = Contact.objects.get(id=contact_id)
    if not contact.email_sent:
        simulate_email_sending(contact.email)
        contact.email_sent = True
        contact.save()
        print(f"Updated contact ID: {contact_id} to email_sent=True")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
