<a target="_blank" href="https://discord.com/oauth2/authorize?client_id=1161496541421391884"><img src="https://dcbadge.limes.pink/api/shield/1161496541421391884?bot=true" alt="" /></a>
<a target="_blank" href="https://www.linkedin.com/in/aarush-kumar-32a414301/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge" /></a>
<a target="_blank" href="https://discord.gg/eaEURGYM8S"><img src="https://dcbadge.limes.pink/api/server/eaEURGYM8S" alt="Discord Server Badge" /></a>

## Table of Contents
1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Commands](#commands)
6. [Customization](#customization)

## Introduction

**Simply** is your ultimate companion in deciphering the complexities of Privacy Policies and Terms of Service. Designed to simplify legal documents effortlessly, Simply helps you understand these daunting documents with ease.

Are you overwhelmed by lengthy, jargon-filled legal agreements? You’re not alone. Simply steps in as your personal assistant, offering clear grades and easy-to-understand summaries that highlight crucial clauses.

Simply supports a variety of file types, including images, PDFs, and text files. It can analyze up to 15 previous messages to provide context and understanding. Worried about your privacy? Simply allows you to reset and clear your message history as needed.

Simply is also multilingual, capable of communicating in over 45 languages. Whether you’re a casual user looking to understand what you’re agreeing to or a frequent navigator of online agreements, Simply is your go-to tool for clarity and simplicity. Best of all, Simply is free to use and extensively trained on a diverse dataset of legal documents.

Discover more about Simply and its features on the [SimplyAI Discord server](https://discord.gg/jDGJms44Cw), where understanding legal terms is made simple.

Created by [Simplify Me](https://simplify-me.com/simply/).

## Key Features

- **AI-Driven Text Responses:** Generate text responses to messages using Google's generative AI.
- **Supports 5+ File Types:** Responds to images, PDFs, text files, and more (Images should be under 2.5 MB).
- **User Message History Management:** Maintains a history of user interactions via Discord IDs, allowing for context-aware conversations.
- **Customizable Settings:** Adjust various parameters like message history length and AI response settings. Learn more in the [Customization](#customization) section.

## Installation

1. Clone the repository:  
```
git clone [https://github.com/your-repo/simply.git](https://github.com/simplifyme7/Simply.git)
cd Simply
```
2. Install the required Python libraries:

```
   pip install -U -r requirements.txt
```
The bot will start listening to messages in the specified channel of your Discord server. It responds to direct mentions or direct replies.

## Configuration

1. Edit the `.env` file and fill in the following values

- `DISCORD_BOT_TOKEN` Your Discord bot token.
- `GOOGLE_AI_KEY` Your Google AI API key. Free Google API Keys can be acquired from [Google AI Studio](https://aistudio.google.com/app/apikey).
- `MAX_HISTORY` The maximum number of messages to retain in history for each user. 0 will disable history
- `TEST_CHANNEL` The name of the channel where you would like to test Simply. (Optional)
- `PUBLIC_CHANNEL` The name of the channel where you would like everyone to use Simply.

2. Run `SimplyAIBot.py`
```
python SimplyAIBot.py
```
   
## Commands

- **Activate Simply**: Mention or reply to Simply to activate it. History only works with pure text input.
- `/reset` Resets and clears the user chat history with Simply. History automatically resets after reaching the `MAX_HISTORY`.
- `/info` Provides basic info and description about Simply.
- `/classification` Describes the classification of grades scored by Simply.

## Customization

(Coming Soon...)
