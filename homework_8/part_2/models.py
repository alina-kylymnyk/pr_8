
from mongoengine import Document, StringField, BooleanField, connect

connect(
    db='email_contacts_db',
    username='your_username',
    password='your_password',
    host='your_cluster_url',
    tls=True
)

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    email_sent = BooleanField(default=False)
    additional_info = StringField()  

    meta = {'collection': 'contacts'}
