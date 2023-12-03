import logging
from datetime import datetime

# Set up logging configuration
logging.basicConfig(filename='atm_service.log', level=logging.INFO)
# Create a logger instance
logger = logging.getLogger(__name__)


# singleton atm service
class AtmService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls.atm_balance = 10000.00
            cls.account_balances = {
                '2859459814': 10.24,
                '1434597300': 90000.55,
                '7089382418': 0.00,
                '2001377812': 60.00
            }
            cls.transaction_history = {
                '2859459814': [],
                '1434597300': [],
                '7089382418': [],
                '2001377812': []
            }

        return cls._instance

    def withdraw(self, account_id, value):
        account_balance = self.account_balances[account_id]
        is_money_available_in_atm = (self.atm_balance - value) >= 0

        # account already overdrawn
        if account_balance < 0:
            logging.warning('Already Overdrawn', {'account_id': account_id})
            return 'Your account is overdrawn! You may not make withdrawals at this time.'

        # empty atm
        # In the real world this should probably send some sort of message to whomever fills the ATM
        # Should also prevent any more users from logging in and display a message like 'Out of service'.
        if self.atm_balance == 0:
            logging.warning('Empty ATM', {'account_id': account_id})
            return 'Unable to process your withdrawal at this time.'

        # must be a multiple of 20
        if value % 20 != 0:
            logging.warning('Not multiple of 20', {'account_id': account_id})
            return 'Please enter a multiple of $20.'

        # doesn't overdraw
        if (not is_money_available_in_atm and account_balance >= self.atm_balance) or account_balance >= value:
            if is_money_available_in_atm:
                self.atm_balance -= value
                self.account_balances[account_id] -= value
                self.write_history(account_id, -value, self.account_balances[account_id])
                logging.info('Withdrawal successful',
                             extra={'account_id': account_id,
                                    'amount': value,
                                    'balance': self.account_balances[account_id]}
                             )
                return f'Amount dispensed: ${value}. \n ' \
                       f'Current balance: ${self.account_balances[account_id]}.'
            else:
                amount_to_dispense = self.atm_balance
                self.atm_balance -= amount_to_dispense
                self.account_balances[account_id] -= amount_to_dispense
                self.write_history(account_id, -amount_to_dispense, self.account_balances[account_id])
                logging.info('Withdrawal successful',
                             extra={'account_id': account_id,
                                    'amount': amount_to_dispense,
                                    'balance': self.account_balances[account_id]}
                             )
                return f'Unable to dispense full amount requested at this time. \n' \
                       f'Amount dispensed: ${amount_to_dispense}. \n ' \
                       f'Current balance: ${self.account_balances[account_id]}.'

        # overdraws
        if (not is_money_available_in_atm and account_balance < self.atm_balance) or account_balance < value:
            if is_money_available_in_atm:
                self.atm_balance -= value
                # user withdrawal
                self.account_balances[account_id] -= value
                self.write_history(account_id, -value, self.account_balances[account_id])
                logging.info('Withdrawal successful',
                             extra={'account_id': account_id,
                                    'amount': value,
                                    'balance': self.account_balances[account_id]}
                             )

                # overdraft fee
                self.account_balances[account_id] -= 5.00
                self.write_history(account_id, -5, self.account_balances[account_id])
                logging.info('Overdraft',
                             extra={'account_id': account_id, 'balance': self.account_balances[account_id]})

                return f'Amount dispensed: ${value}. \n ' \
                       f'You have been charged an overdraft fee of $5. ' \
                       f'Current balance: ${self.account_balances[account_id]}.'
            else:
                amount_to_dispense = self.atm_balance
                self.atm_balance -= amount_to_dispense
                self.account_balances[account_id] -= amount_to_dispense
                self.write_history(account_id, -amount_to_dispense, self.account_balances[account_id])
                logging.info('Withdrawal successful',
                             extra={'account_id': account_id,
                                    'amount': value,
                                    'balance': self.account_balances[account_id]}
                             )

                self.account_balances[account_id] -= 5.00
                self.write_history(account_id, -5, self.account_balances[account_id])
                logging.info('Overdraft',
                             extra={'account_id': account_id, 'balance': self.account_balances[account_id]})

                return f'Unable to dispense full amount requested at this time. \n' \
                       f'Amount dispensed: ${amount_to_dispense}. \n ' \
                       f'You have been charged an overdraft fee of $5. ' \
                       f'Current balance: ${self.account_balances[account_id]}.'

    def deposit(self, account_id, value):
        if value <= 0:
            logging.warning('Negative deposit attempted', {'account_id': account_id})
            return 'Please deposit an amount greater than zero.'
        self.account_balances[account_id] += value
        self.write_history(account_id, value, self.account_balances[account_id])
        logging.info('Deposit successful',
                     extra={'account_id': account_id,
                            'amount': value,
                            'balance': self.account_balances[account_id]}
                     )
        return f'Current balance: {self.account_balances[account_id]}.'

    def get_balance(self, account_id):
        try:
            return f'Current Balance: ${self.account_balances[account_id]}'
        except KeyError:
            return 'Account not found.'

    def write_history(self, account_id, value, balance):
        formatted_date = datetime.now().date().strftime('%Y-%m-%d')
        formatted_time = datetime.now().time().strftime('%H:%M:%S')

        history = [formatted_date, formatted_time, value, balance]
        # inserting at the start of the list
        self.transaction_history[account_id].insert(0, history)

    def get_history_by_account_id(self, account_id):
        try:
            account_history = self.transaction_history[account_id]
        except KeyError:
            return 'No history found.'

        if account_history:
            history_string = f''
            for event in account_history:
                history_string += f'{event[0]} {event[1]} {event[2]} {event[3]} \n'
            return history_string[:len(history_string) - 2]
        else:
            return 'No history found.'









