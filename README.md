# -Console Assistant Bot-

<p align="center">This is a simple console-based assistant bot prototype that can manage contacts. It recognizes various commands and responds accordingly.</p>

## 🚀 Features

- Add a new contact with name and phone number.
- Change the phone number of an existing contact.
- Retrieve the phone number of a contact.
- Display all saved contacts with their phone numbers.
- End the interaction with the bot.

## 💡 Usage

1. Run the script `main.py` in your console.
2. The bot will be waiting for your commands.
3. Available commands:

   - `hello`: Greet the bot.
   - `add [name] [phone] [birthday]`: Add a new contact with the specified name and phone number.
   - `change [name] [phone]`: Change the phone number of an existing contact.
   - `phone [name]`: Retrieve the phone number of a contact.
   - `show all`: Display all saved contacts.
   - `days to birthday` -> `[name]`: The number of days until the next birthday.
   - `good bye`, `close`, `exit`: End the interaction with the bot.

## 🛠️ Implementation Details

The bot uses a dictionary to store contacts, where the name is the key and the phone number is the value. The bot also handles input errors gracefully using the `input_error` decorator.

## 🏃 Running the Bot

To run the bot, make sure you have Python installed and execute the following command in your terminal:

```bash
python main.py
