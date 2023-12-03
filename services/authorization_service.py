import time
import logging

# Set up logging configuration
logging.basicConfig(filename='authorization_service.py', level=logging.INFO)
# Create a logger instance
logger = logging.getLogger(__name__)


# singleton authorization service
class AuthorizationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls.account_information = {
                '2859459814': '7386',
                '1434597300': '4557',
                '7089382418': '0075',
                '2001377812': '5950'
            }

            cls.account_activity = {}
        return cls._instance

    # function to initially authorize users
    def authorize(self, account_id, entered_pin):
        self.logout()  # logout any currently logged in account

        # validate auth request
        if account_id not in self.account_information:
            logging.warning('Bad auth. Wrong account_id.')
            return 'Authorization failed.'

        expected_pin = self.account_information[account_id]
        if entered_pin != expected_pin:
            logging.warning('Bad auth. Wrong pin.', {'account_id': account_id})
            return 'Authorization failed.'

        self.account_activity[account_id] = time.time()
        logging.info('Successful Authorization', extra={'account_id': account_id})

        return f'{account_id} successfully authorized.'

    def logout(self):
        account_id = list(self.account_activity.keys())[0] if self.account_activity else None
        if not account_id:
            return 'No account is currently authorized.'

        del self.account_activity[account_id]
        logging.info('Logout', extra={'account_id': account_id})
        return f'Account {account_id} logged out.'

    def get_active_account_id(self):
        return list(self.account_activity.keys())[0] if self.account_activity else None

    def is_authorization_active(self):
        if not self.account_activity:
            return False
        account_id, activity_time_in_sec = list(self.account_activity.items())[0]
        current_time_in_seconds = time.time()
        difference = current_time_in_seconds - activity_time_in_sec
        if difference > 120:
            # if account has been inactive for over 2 minutes, log them out
            self.logout()
            return False
        return True

    def refresh_activity(self, account_id):
        self.account_activity[account_id] = time.time()
