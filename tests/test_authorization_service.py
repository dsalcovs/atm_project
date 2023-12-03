import pytest
from services.authorization_service import AuthorizationService
import time


class TestAuthorizationService:

    @pytest.fixture
    def authorization_service(self):
        return AuthorizationService()

    # authorize
    def test_authorize_successful(self, authorization_service):
        account_id = '2859459814'
        correct_pin = '7386'

        result = authorization_service.authorize(account_id, correct_pin)

        assert result == f'{account_id} successfully authorized.'
        assert account_id in authorization_service.account_activity

    def test_authorize_successful_when_different_account_already_authorized(self, authorization_service):
        account_id_1 = '2859459814'
        correct_pin_1 = '7386'

        account_id_2 = '1434597300'
        correct_pin_2 = '4557'

        authorization_service.authorize(account_id_1, correct_pin_1)
        result = authorization_service.authorize(account_id_2, correct_pin_2)

        assert result == f'{account_id_2} successfully authorized.'
        assert account_id_1 not in authorization_service.account_activity
        assert account_id_2 in authorization_service.account_activity

    def test_authorize_failed_invalid_account(self, authorization_service):
        invalid_account_id = '9999999999'
        correct_pin = '7386'

        result = authorization_service.authorize(invalid_account_id, correct_pin)

        assert result == 'Authorization failed.'
        assert invalid_account_id not in authorization_service.account_activity

    def test_authorize_failed_invalid_pin(self, authorization_service):
        account_id = '2859459814'
        incorrect_pin = '0000'  # Incorrect PIN for the account

        result = authorization_service.authorize(account_id, incorrect_pin)

        assert result == 'Authorization failed.'
        assert account_id not in authorization_service.account_activity

    # logout
    def test_logout_successful(self, authorization_service):
        account_id, pin = '2859459814', '7386'
        authorization_service.authorize(account_id, pin)

        result = authorization_service.logout()

        assert result == f'Account {account_id} logged out.'
        assert account_id not in authorization_service.account_activity

    def test_logout_no_account_authorized(self, authorization_service):
        result = authorization_service.logout()
        assert result == 'No account is currently authorized.'

    # get_active_account_id
    def test_get_active_account_id_with_active_account(self, authorization_service):
        account_id = '2859459814'
        authorization_service.authorize(account_id, '7386')

        active_id = authorization_service.get_active_account_id()

        assert active_id == account_id

    def test_get_active_account_id_without_active_account(self, authorization_service):
        # make sure there isn't an active account from a previous test
        authorization_service.logout()
        active_id = authorization_service.get_active_account_id()

        assert active_id is None

    # is_authorization_active
    def test_is_login_active_within_time_limit(self, authorization_service, mocker):
        mocker.patch('time.time', return_value=0)  # Mock time.time() to return 0 for simplicity
        authorization_service.authorize('2859459814', '7386')
        assert authorization_service.is_authorization_active() is True

    def test_is_login_active_past_time_limit(self, authorization_service, mocker):
        authorization_service.authorize('2859459814', '7386')
        mocker.patch('time.time', return_value=time.time() + 500)  # Mock time.time() to return 500 seconds more
        assert authorization_service.is_authorization_active() is False

    def test_is_login_active_without_active_login(self, authorization_service):
        # make sure there isn't an active account from a previous test
        authorization_service.logout()
        assert authorization_service.is_authorization_active() is False

    # refresh_activity
    def test_refresh_activity(self, authorization_service, mocker):
        mocker.patch('time.time', return_value=100)  # Mock time.time() to simulate current time as 100 seconds
        authorization_service.authorize('2859459814', '7386')

        mocker.patch('time.time', return_value=200)  # Mock time.time() after some time has passed (200 seconds)
        authorization_service.refresh_activity('2859459814')

        # Assert that the account's activity time has been updated
        assert authorization_service.account_activity['2859459814'] == 200
