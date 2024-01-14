# Banking System Application

The Banking System Application is a straightforward implementation following clean architecture principles. It encompasses entities for accounts, transactions, and customers, incorporating use cases for creating accounts, making transactions, and generating account statements.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Overview

The application adheres to clean architecture principles, structuring itself into three layers: Domain, Use Case, and Infrastructure. Within the Domain layer, entities such as Account, Transaction, and Customer are defined. The Use Case layer hosts the business logic for creating accounts, performing transactions, and generating statements. The Infrastructure layer manages the interaction between the application and the external world, including data repositories.

## Getting Started

### Prerequisites

- Python 3.x (tested with Python 3.9.6)
- SQLite (for the local database)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lavkushg09/banking_system.git
   ```

2. **Change to the project directory:**
   ```bash
   cd banking_system
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Usage
A sample code is included in the repository to demonstrate the application's functionalities. Execute the following command:

```bash
python sample_script.py
```

Unit test cases are also provided in the repository. To run these test cases, execute the following command in the banking_system folder:

```bash
python test_banking_system.py
```

If you intend to use the code in a different script and want to use SQLite locally, ensure to run the following command to initialize the database schema:

```bash
from db.local_db_initialization import DatabaseInitializer

# Initialize the database
database_initializer = DatabaseInitializer()
database_initializer.initialize_db()

```

### License
This project is licensed under the MIT License.