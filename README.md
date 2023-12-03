### ATM Project

### Requirements:
- Ensure that you have Python installed on your system.

### Steps:

1. **Install Poetry:**
   If you haven't installed Poetry on your system, use Homebrew on macOS or follow the official installation guide from the [Poetry documentation](https://python-poetry.org/docs/#installation).

2. **Navigate to the Project Directory:**
   Open your terminal and navigate to the root directory of the cloned repository using the `cd` command.

3. **Install Project Dependencies:**
   Run the following command to let Poetry install the project dependencies mentioned in `pyproject.toml`:
   ```bash
   poetry install
   ```
   This will create a virtual environment for your project and install all the required dependencies.

4. **Activate the Virtual Environment:**
   Poetry automatically creates a virtual environment for each project. To activate it, use:
   ```bash
   poetry shell
   ```
   This will activate the virtual environment, allowing you to work within its isolated Python environment.

5. **Run the Program:**
   Once the virtual environment is activated, you can run your program using Python. Execute:
   ```bash
   python main.py
   ```
   This command will start the ATM program.

### ATM Program Instructions

This program mimics an ATM experience, allowing you to perform various actions. Use the following commands to interact:

#### Commands:

1. **Authorize an Account**:
   - Enter your account ID and PIN to access your account.
   - Example: `authorize <account_id> <pin>`

2. **Withdraw Money**:
   - Withdraw cash in multiples of $20 from your account.
   - Example: `withdraw <value>`

3. **Deposit Funds**:
   - Add money to your account. Value must be greater than zero.
   - Example: `deposit <value>`

4. **Check Balance**:
   - View your current account balance.
   - Example: `balance`

5. **Transaction History**:w
   - Retrieve a record of your recent transactions.
   - Example: `history`

6. **Log Out**:
   - Sign out of your account to ensure security.
   - Example: `logout`

7. **End Program**:
   - Exit the ATM program.
   - Example: `end`
---
