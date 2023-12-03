from services.atm_service import AtmService
from services.authorization_service import AuthorizationService

authorization_service = AuthorizationService()
atm_service = AtmService()


def process_command(command, *args):
    if command.lower() == 'authorize':
        try:
            account_id = args[0]
            pin = args[1]
            return authorization_service.authorize(account_id, pin)
        except (ValueError, IndexError) as e:
            return 'Authorization failed.'
    elif command.lower() == 'logout':
        return authorization_service.logout()

    # no account has been logged into
    account_id = authorization_service.get_active_account_id()
    if not account_id:
        return 'Authorization Required.'

    # don't allow accounts to continue running commands after 2 minutes of inactivity
    is_login_active = authorization_service.is_authorization_active()
    if not is_login_active:
        return 'Your login has time out. Please reauthorize.'

    # if we have an active account logged in we should refresh their activity tracker
    authorization_service.refresh_activity(account_id)

    # user commands that require an authorized and active account
    if command.lower() == 'withdraw':
        value = args[0]
        return atm_service.withdraw(account_id, int(value))
    elif command.lower() == 'deposit':
        value = args[0]
        return atm_service.deposit(account_id, float(value))
    elif command.lower() == 'balance':
        return atm_service.get_balance(account_id)
    elif command.lower() == 'history':
        return atm_service.get_history_by_account_id(account_id)
    else:
        return 'Command not recognized. Please try again.'


def main():
    print('Welcome to my ATM! Please login.')

    while True:
        user_input = input('> ')  # Prompt the user for input

        if user_input.lower() == 'end':
            break  # Exit the loop and end the program

        parts = user_input.split()  # Split the input into parts
        command = parts[0]
        args = parts[1:]

        result = process_command(command, *args)
        print(result)


if __name__ == "__main__":
    main()

