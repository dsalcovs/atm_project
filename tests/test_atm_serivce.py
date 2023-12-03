import pytest
from datetime import datetime

from services.atm_service import AtmService


class TestAtmService:

    @pytest.fixture
    def atm_service(self):
        return AtmService()

    # withdraw
    # Normal withdrawal scenarios
    def test_withdraw_successful(self, atm_service):
        atm_service.account_balances['2859459814'] = 100  # Setting a balance for testing
        atm_service.atm_balance = 500  # Setting ATM balance for testing

        result = atm_service.withdraw('2859459814', 80)

        date = datetime.now().date().strftime('%Y-%m-%d')
        time = datetime.now().time().strftime('%H:%M:%S')

        expected_history = [
            [date, time, 50, 170],
            ['2023-11-30', '15:30:45', 30, 120]  # Existing data
        ]

        assert result == 'Amount dispensed: $80. \n Current balance: $20.'

    def test_withdraw_partial_amount(self, atm_service):
        atm_service.account_balances['2859459814'] = 100  # Setting a balance for testing
        atm_service.atm_balance = 500  # Setting ATM balance for testing

        result = atm_service.withdraw('2859459814', 60)

        assert result == 'Amount dispensed: $60. \n Current balance: $40.'

    def test_withdraw_all_account_balance(self, atm_service):
        atm_service.account_balances['2859459814'] = 100  # Setting a balance for testing
        atm_service.atm_balance = 500  # Setting ATM balance for testing

        result = atm_service.withdraw('2859459814', 100)

        assert result == 'Amount dispensed: $100. \n ' \
                         'Current balance: $0.'

    # Overdrawn account scenarios
    def test_withdraw_overdrawn_account(self, atm_service):
        atm_service.account_balances['2859459814'] = -50  # Simulating an overdrawn account
        atm_service.atm_balance = 100  # Setting ATM balance for testing

        result = atm_service.withdraw('2859459814', 30)

        assert result == 'Your account is overdrawn! You may not make withdrawals at this time.'

    # Empty ATM scenarios
    def test_withdraw_no_money_in_atm(self, atm_service):
        atm_service.account_balances['2859459814'] = 200  # Setting a balance for testing
        atm_service.atm_balance = 0  # Simulating an empty ATM

        result = atm_service.withdraw('2859459814', 50)

        assert result == 'Unable to process your withdrawal at this time.'

    # Invalid withdrawal amount scenarios
    def test_withdraw_invalid_amount(self, atm_service):
        atm_service.account_balances['2859459814'] = 200  # Setting a balance for testing
        atm_service.atm_balance = 500  # Setting ATM balance for testing

        result = atm_service.withdraw('2859459814', 35)

        assert result == 'Please enter a multiple of $20.'

    # Withdrawal exceeding ATM balance scenarios
    def test_withdraw_exceed_atm_balance(self, atm_service):
        atm_service.account_balances['2859459814'] = 200  # Setting a balance for testing
        atm_service.atm_balance = 50  # Setting a low ATM balance for testing

        result = atm_service.withdraw('2859459814', 80)

        assert result == 'Unable to dispense full amount requested at this time. \n' \
                         'Amount dispensed: $50. \n Current balance: $150.'

    # Withdrawal exceeding account balance scenarios
    def test_withdraw_exceed_account_balance(self, atm_service):
        atm_service.account_balances['2859459814'] = 100  # Setting a balance for testing
        atm_service.atm_balance = 500  # Setting ATM balance for testing

        result = atm_service.withdraw('2859459814', 120)

        assert result == 'Amount dispensed: $120. \n ' \
                         'You have been charged an overdraft fee of $5. ' \
                         'Current balance: $-25.0.'

    def test_withdraw_account_already_overdrawn(self, atm_service):
        atm_service.account_balances['2859459814'] = -50  # Simulating an overdrawn account
        atm_service.atm_balance = 500  # Setting ATM balance for testing

        result = atm_service.withdraw('2859459814', 50)

        assert result == 'Your account is overdrawn! You may not make withdrawals at this time.'

    # deposit
    def test_deposit_successful(self, atm_service):
        atm_service.account_balances['2859459814'] = 100  # Setting a balance for testing

        result = atm_service.deposit('2859459814', 50)

        assert result == 'Current balance: 150.'

    def test_deposit_decimal_value(self, atm_service):
        atm_service.account_balances['2859459814'] = 100  # Setting a balance for testing

        result = atm_service.deposit('2859459814', 10.10)

        assert result == 'Current balance: 110.1.'

    def test_deposit_zero_value(self, atm_service):
        atm_service.account_balances['2859459814'] = 100  # Setting a balance for testing

        result = atm_service.deposit('2859459814', 0)

        assert result == 'Please deposit an amount greater than zero.'

    def test_deposit_negative_value(self, atm_service):
        atm_service.account_balances['2859459814'] = 100  # Setting a balance for testing

        result = atm_service.deposit('2859459814', -50)

        assert result == 'Please deposit an amount greater than zero.'

    # get_balance
    def test_get_balance_existing_account(self, atm_service):
        atm_service.account_balances['2859459814'] = 100  # Setting a balance for testing

        result = atm_service.get_balance('2859459814')

        assert result == 100

    def test_get_balance_non_existing_account(self, atm_service):
        result = atm_service.get_balance('0000000000')  # Non-existing account

        assert result == 'Account not found.'

    # write_history
    def test_write_history_valid_data(self, atm_service):
        atm_service.transaction_history['2859459814'] = []  # Initializing history for testing
        date = datetime.now().date().strftime('%Y-%m-%d')
        time = datetime.now().time().strftime('%H:%M:%S')

        atm_service.write_history('2859459814', 50, 150)  # Example data for history

        expected_history = [
            [date, time, 50, 150]
        ]
        assert atm_service.transaction_history['2859459814'] == expected_history

    def test_write_history_existing_data(self, atm_service):
        atm_service.transaction_history['2859459814'] = [[
            '2023-11-30', '15:30:45', 30, 120
        ]]  # Initializing history for testing

        date = datetime.now().date().strftime('%Y-%m-%d')
        time = datetime.now().time().strftime('%H:%M:%S')

        atm_service.write_history('2859459814', 50, 170)  # Example data for history

        expected_history = [
            [date, time, 50, 170],
            ['2023-11-30', '15:30:45', 30, 120]  # Existing data
        ]
        assert atm_service.transaction_history['2859459814'] == expected_history

    # get_history_by_account_id
    def test_get_history_existing_data(self, atm_service):
        atm_service.transaction_history['2859459814'] = [
            ['2023-11-30', '15:30:45', 50, 150],
            ['2023-11-29', '10:20:30', 30, 100]
        ]  # Simulating existing history

        result = atm_service.get_history_by_account_id('2859459814')

        assert result == '2023-11-30 15:30:45 50 150 \n2023-11-29 10:20:30 30 100'

    def test_get_history_no_data(self, atm_service):
        result = atm_service.get_history_by_account_id('1434597300')  # Non-existing account

        assert result == 'No history found.'
