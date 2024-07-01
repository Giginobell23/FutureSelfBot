
# FutureSelfBot

FutureSelfBot is a Telegram bot that allows users to schedule emails to be sent to their future selves. Use it to set reminders, send motivational messages, or reflect on your goals and dreams. 

## Features

- **Schedule Emails**: Easily schedule emails to be delivered at a future date and time.
- **User-friendly Interface**: Interact with the bot through a simple and intuitive Telegram chat interface.
- **Secure Delivery**: Ensures secure and reliable email delivery.

## Getting Started

### Prerequisites

- Python 3.7+
- Telegram account
- Email account for sending emails

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/FutureSelfBot.git
    cd FutureSelfBot
    ```

2. **Create a virtual environment and activate it**:

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies**:

4. **Configure the bot**:

    - Edit `config.py` to include your Telegram bot token and email credentials.

5. **Run the bot**:

    ```bash
    python bot.py
    ```

## Usage

1. **Start a chat with FutureSelfBot on Telegram**.
2. **Follow the prompts** to schedule your future email.
3. **Wait** for your message to arrive on the specified date.

## Configuration

In `constants.py`, you need to set the following configurations:

- `TELEGRAM_TOKEN`: Your Telegram bot token.
- `SENDER_EMAIL`: The email address from which emails will be sent.
- `SENDER_PASSWORD`: The password for the email account.


## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any features, bug fixes, or enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
