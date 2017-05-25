# telegram-vk-bridge

Telegram bot to write messages to VK from Telegram 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development. See deployment for notes on how to deploy the project on a live system.

### Installing

To install the bot copy its repository to your machine

    git clone https://github.com/pythad/telegram-vk-bridge.git

Then install requirements for your local virtualenv with


    pip install -r requirements.txt

Set environment variables with:


    export TELEGRAM_TOKEN="YOUR_TELEGRAM_TOKEN"
    export VK_USERNAME="YOUR_VK_USERNAME"
    export VK_PASSWORD="YOUR_VK_PASSWORD"
    export VK_RECIPIENT=VK_RECIPIENT_ID


Now you can run the bot with `python main.py`

## Deployment

The project is production ready. Feel free to check [this article](https://askubuntu.com/questions/396654/how-to-run-the-python-program-in-the-background-in-ubuntu-machine) in order to learn how to run bot in the background

## Built With

* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram API wrapper for Python
* [vk_api](https://github.com/python273/vk_api) - VK API wrapper for Python

## Authors

* **Vlad Ovchynnykov** - *Initial work* - [pythad](https://github.com/pythad)