# Meet Simply: Your New Tool for Decoding Legalese

Introducing Simply, your ultimate companion in deciphering the complexities of Privacy Policies and Terms of Service! Simply is designed to simplify legal documents effortlessly.

Do you find Privacy Policies and Terms of Service daunting? You’re not alone. They’re often lengthy, filled with confusing jargon, and difficult to navigate. Simply steps in as your personal assistant, offering clear grades and easy-to-understand summaries that highlight crucial clauses.

Simply supports a variety of file types, including images, PDFs, and text files. It can analyze up to 15 previous messages to provide context and understanding. Worried about your privacy? Simply allows you to reset and clear your message history as needed.

While Simply excels in understanding legal jargon, it’s also multilingual, capable of communicating in over 45 languages. Whether you’re a casual user looking to understand what you’re agreeing to or a frequent navigator of online agreements, Simply is your go-to tool for clarity and simplicity. Best of all, Simply is free to use and extensively trained on a diverse dataset of legal documents.

With Simply by your side, navigating the legal landscape has never been easier. Discover more about Simply and its features on the SimplyAI discord server, where understanding legal terms is made simple.

## Key Features

- **AI-Driven Text Responses:** Simply can generate text responses to messages using Google's generative AI.
- **5+ File Types Supported:** Simply can also respond to images, PDFs, text files and more. (Images should be under 2.5 Megs)
- **User Message History Management:** Simply maintains a history of user interactions via discordIDs, allowing for context-aware conversations.
- **Customizable Settings:** Users can adjust various parameters like message history length and AI response settings. Learn more in the [Customization](#customization) section.

## Installation

1. Clone the repository to your local machine.
2. Install the required Python libraries:

   ```
   pip install -U -r requirements.txt
   ```
The bot will start listening to messages in the specific channel of your Discord server. It responds to direct mentions or direct replies.

## Configuration

1. Edit the `.env` file and fill in the following values

- `DISCORD_BOT_TOKEN`: Your Discord bot token
- `GOOGLE_AI_KEY`: Your Google AI API key. Google API Key can be acquired from https://makersuite.google.com/
- `MAX_HISTORY`: The maximum number of messages to retain in history for each user. 0 will disable history
- `TEST_CHANNEL`: The name of the channel where you would like to test Simply. (Optional)
- `PUBLIC_CHANNEL`: The name of the channel where you would like everyone to use Simply.

2. Run `SimplyAIBot.py`

## Commands

- **Mention or reply to the bot to activate:** History only works on pure text input
- `/reset`: Resets and clears the user chat history with the bot. History automatically resets after 15 messages.
- `/info`: Provides basic info and description about Simply.
- `/classification`: Describes the classification of grades scored by Simply.

## Discord

- You can join the official SimplyAI discord server and use Simply for free at https://discord.gg/jDGJms44Cw
- Optionally, you can also add Simply to your own server with https://discord.com/oauth2/authorize?client_id=1161496541421391884

## Customization
