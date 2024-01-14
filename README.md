# Banking System Application

This is a simple banking system application that follows the clean architecture principles. It includes entities for accounts, transactions, and customers, along with use cases for creating accounts, making transactions, and generating account statements.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Overview

The application is structured using the clean architecture principles with three layers: Domain, Use Case, and Infrastructure. Entities such as Account, Transaction, and Customer are defined in the Domain layer. The Use Case layer contains business logic for creating accounts, making transactions, and generating statements. The Infrastructure layer deals with the interaction between the application and the outside world, including the data repository.

## Getting Started

### Prerequisites

- Python 3.x  (tested with Python 3.9.6)
- SQLite (for the local database)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/banking-system.git
