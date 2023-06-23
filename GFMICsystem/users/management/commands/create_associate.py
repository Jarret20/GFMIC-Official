from users.models import Membership
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create an Admin User'

    def add_arguments(self, parser) -> None:
        parser.add_argument('m_no', type=str, help='enter admin m_no.')
        parser.add_argument('email', type=str, help='enter admin email.')
        parser.add_argument('password', type=str, help='enter admin password.')

    def handle(self, *args, **kwargs):
        m_no = kwargs['m_no']
        m_email = kwargs['email']
        m_password = kwargs['password']
        member = Membership(
            user_no = m_no,
            user_email= m_email,
            user_password = m_password,
            user_sub='ASSOCIATE',
            user_status = 'ACTIVE',
        )
        member.save()
