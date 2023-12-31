# Railways Management System

**Railways Management System** is a comprehensive Python project for managing railway operations. This system provides functionalities for ticket booking, payment verification, and ticket cancellation. It offers an easy-to-use command-line interface for users and administrators.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🎫 **Ticket Booking System:** Users can book train tickets based on their preferences.
- 💰 **Payment Verification:** Admins can verify and process pending payments for booked tickets.
- 🗃️ **Manage Booked Tickets:** Admins can search, cancel, or view details of booked tickets.
- 🌐 **Role-Based Access:** Multi-user support with different roles, such as user and admin.
- 📊 **Transaction History:** Users can view their booked tickets and their status.
- 🚂 **Train Schedule:** Display the schedule of available trains.

## Installation

1. **Clone the repository for Linux Users:**

   ```bash
   git clone https://github.com/BinaryGhostDev/Railways.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd Railways
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Update these details from `config.py`:**
   - `user="your_username"`
   - `password="your_password"`
   - `database="your_database_name"`

   Admin Login Details:
   - Username: RajanGoswami
   - Password: admin

   or

   - Username: admin
   - Password: admin
  
5. **Run the application:**

   - Main File (Always Run This Main File):

     ```bash
     python main.py
     ```
     
   - For users:

     ```bash
     python user.py
     ```

   - For admins:

     ```bash
     python admin.py
     ```

## Usage

### User Interface:

1. **Book a Ticket:**

   - Select a train, enter journey details, and proceed with the booking.

2. **View Transaction History:**

   - Check the status of booked tickets.

### Admin Interface:

1. **Verify Payments:**

   - Admins can view pending payments, verify them, and update the payment status.

2. **Manage Booked Tickets:**

   - Search tickets by PNR, view all booked tickets, cancel tickets, or view tickets by user ID.

3. **Train Schedule:**

   - Admins can view the schedule of available trains.

## Contributing

*Contributions are welcome! Please follow these guidelines:*

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
