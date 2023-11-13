---
Project name: Django_tatum
Topic: Startup instructions
---


1. Please see this article on using poetry to manage virtualenvironments:

[Using to Poetry with Django]("https://rasulkireev.com/managing-django-with-poetry/"){target="_blank"}

Here is the poetry doc for installing dependencies to the project:
["https://python-poetry.org/docs/basic-usage/#installing-dependencies"]{target="_blank"}

2. Preferably, use this command to create a virtual in the same directory as the current directory:

> poetry config virtualenvs.in-project true

3. To activate virtualenv from default directory of installation:
> source $(poetry env info --path)/bin/activate

3. For populating requirements.txt, use this command:
	> poetry export -f requirements.txt --output requirements.txt

4.[Connect Azure Postgres instance to pgAdmin4]("https://www.sqlshack.com/accessing-azure-database-for-postgresql-using-pgadmin/"){target="_blank"}

5. [Running cron jobs with django extensions]('https://django-extensions.readthedocs.io/en/latest/jobs_scheduling.html'){target="_blank"}
6. [Graphene bug fix]('https://stackoverflow.com/questions/70382084/import-error-force-text-from-django-utils-encoding'){target="_blank"}

===========================
Quick Start
===========================

1. Add "tatum" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "tatum",
    ]

2. Include the tatum URLconf in your project urls.py like this::

    path("tatum/", include("tatum.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/tatum/


===========================
Testing Phase
===========================
To create a blockcahin deposit address on an ethereum chain:

1. Generating an Ethereum Wallet
  To create an Ethereum wallet, follow these steps:

        if __name__ == "__main__":
            ethereum = EthereumWallet()
            eth_wallet = ethereum.generate_ethereum_wallet()
            print(eth_wallet)
  Running the code with python -m ethereum or python ethereum.py will generate a mnemonic and xpub, like this:
        {'xpub': 'your xpub', 'mnemonic': 'your mnemonic'}

2. Creating a Virtual Account
  To create a virtual account, you need to provide the generated xpub and the currency of the blockchain. Here's how to do it:

        if __name__ == "__main":
            tatum_virtual_account = TatumVirtualAccounts()
            data = {"currency": "ETH", "xpub": "input your extended public"}
            tvc = tatum_virtual_account.generate_virtual_account(data)
            print(tvc)
  Running the code with python -m account or python account.py will generate a virtual account alongside a virtual account ID.

3. Creating a Blockchain Address
  After generating the ID of the virtual account, you can create a blockchain address and link it to the virtual account:

        if __name__ == "__main__":
            tatum_blockchain_address = TatumBlockchainAdress()
            id = "input your ID"
            tba = tatum_blockchain_address.create_deposit_address(id)
            print(tba)
  Running the code with python -m blockcahin_address or python blockcahin_address.py will generate an Ethereum blockchain address, which contains:
        {'xpub': 'your xpub', 'derivationKey': 'your derivation key', 'address': 'your address will be generated', 'currency': 'ETH'}



====================================
Running Nox Sessions in Django_tatum
====================================

This project uses Nox for automation of various development tasks, including testing, type checking, and code formatting. The Nox sessions are configured to work seamlessly with Poetry, our tool for dependency management and packaging.
Prerequisites

Before running the Nox sessions, ensure you have the following installed:

    Python (versions 3.8, 3.9, 3.10)
    Poetry
    Nox

Install all dependencies with poetry

    ```bash
    poetry install
    ```

Available Nox Sessions

    tests: Run tests using Pytest across multiple Python versions (3.8, 3.9, 3.10).
    mypy: Perform type checking with MyPy.
    pre_commit: Run pre-commit hooks on all files.
    black: Format all Python code using Black.

Running Nox Sessions

To run a specific Nox session:

    Open a terminal in the project's root directory.

    Use Poetry to activate the virtual environment (if not already activated) and run the desired Nox session.
    For example, to run the pre-commit session, use:


```bash
    poetry run nox -s pre-commit
```

***Please see the noxfile.py for the list of all sessions available.***

Running All Sessions

To run all Nox sessions sequentially:

    Use the following command:

    ```bash
    poetry run nox
    ```
    This will execute each session as defined in the noxfile.py.

Considerations

    Session Isolation: Each Nox session runs in an isolated environment. Dependencies are installed as needed per session.
    Performance: Running multiple sessions, especially across different Python versions, can take time. Consider running only necessary sessions for your development tasks.
    Pre-commit Hooks: If the pre_commit session fails, it typically indicates issues with code style or other checks defined in the pre-commit configuration. Resolve these before committing your code.
    Code Formatting with Black: Running the black session will modify your code to conform to Black's style. Review changes before committing.
    Type Checking with MyPy: The mypy session will check for type consistency in your code. Address any type-related issues highlighted by MyPy.
