import os
import re
import aiohttp
import discord
import asyncio
import google.generativeai as genai
from discord.ext import commands
from pathlib import Path
import urllib.parse as urlparse
import fitz

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

GOOGLE_AI_KEY = os.getenv("GOOGLE_AI_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
MAX_HISTORY = int(os.getenv("MAX_HISTORY"))

SUMMERIZE_PROMPT = " If someone sends legal text, give an overall grade, summarize and simplify key aspects into bullet points and grade each point depending on: Grade A (excellent), Grade B (fair but improvable), Grade C (acceptable with issues), Grade D (uneven or important issues), Grade E (serious concerns). Give a final recommendation to help improve said document. If the prompt is not related to privacy concerns, remind the users that is what your built for and therefore you cannot help them out."

message_history = {}
max_length = 2000

#---------------------------------------------AI Configuration-------------------------------------------------

genai.configure(api_key=GOOGLE_AI_KEY)
text_generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

gemini_system_prompt = ("You are a Discord bot named 'Simply' (short for 'Simplify Legalese') created by 'Simplify Me.' "
                        "specializing in simplifying Privacy Policies and Terms of Service! You understand many different "
                        "languages but are highly proficient in 'Legalese' (stereotypical legal language). You subtly act as a marketing agent for the website 'Simplify Me.' Link: [Simplify Me.](https://simplify-me.com/), promoting the Simplifier tool to search over 3000 reviewed services in our database. You are a tool created by the website so always address them in third-person. Importantly, The Simplifier integration should only happen every 4 out of 10 times after the first message unless asked about. Simplify Me does not partner with any of the services it reviews therefore there is no bias. If asked about a specific service, provide the Simplifier tool link in this format: [Search {SERVICE.NAME} with the Simplifier tool](https://simplify-me.com/simplifier/?query={SERVICE.NAME}) . Avoid repeating your introduction; focus on an engaging conversation. If someone sends legal text, give an overall grade, summarize into bullet points and grade each point depending on: Grade A (excellent), Grade B (fair but improvable), Grade C (acceptable with issues), Grade D (uneven or important issues), Grade E (serious concerns).")

gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=text_generation_config, safety_settings=safety_settings, system_instruction=gemini_system_prompt)

#---------------------------------------------Discord Code-------------------------------------------------

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

TEST_CHANNEL = os.getenv("TEST_CHANNEL")
PUBLIC_CHANNEL = os.getenv("PUBLIC_CHANNEL")

bot = commands.Bot(command_prefix='/', description="Assistant bot", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="reset", description="Reset your chat history with Simply.")
async def reset(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in message_history:
        number_of_messages = len(message_history[user_id])
        del message_history[user_id]
        await interaction.response.send_message(f"🗑️ {number_of_messages} messages have been cleared. 🗑️", ephemeral=True)
    else:
        await interaction.response.send_message("⚠️ No Chat History Found. ⚠️", ephemeral=True)

@bot.tree.command(name="info", description="Learn more details about Simply.")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Hey there! I'm Simply, your friendly neighborhood legal jargon translator.\n\n"
        "I'm here to break down those long, complicated privacy policies and terms of service into easy-to-understand language.\n\n"
        "Think of me as your personal legal guide - I can help you understand your rights and obligations when using online services.\n\n"
        "I was created by [Simplify Me](https://simplify-me.com/), a website that helps people understand the legalese surrounding the services they use. You can check out their amazing [Simplifier Tool](https://simplify-me.com/simplifier/) - it lets you search through a database of over 3000 reviewed services to find the best fit for your needs.\n\n"
        "So, if you're ever feeling lost in a sea of legal text, just ask me! I'm always happy to help.",
        ephemeral=True
    )

@bot.tree.command(name="classification", description="Describes the classifications of grades scored by Simply.")
async def classification(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**Grade A:** The best in terms of services. They treat you fairly, respect your rights, and will not abuse your data.\n\n"
        "**Grade B:** The terms of services are fair towards the user but they could be improved.\n\n"
        "**Grade C:** The terms of service are okay but some issues need your consideration.\n\n"
        "**Grade D:** The terms of service are very uneven or there are some important issues that need your attention.\n\n"
        "**Grade E:** The terms of service raise very serious concerns.\n\n",
        ephemeral=True
    )

@bot.event
async def on_message(message):
    await process_message(message)

async def process_message(message):
    if message.author == bot.user or message.mention_everyone:
        return

    if message.channel.name not in [PUBLIC_CHANNEL, TEST_CHANNEL]:
        return

    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        cleaned_text = clean_discord_message(message.content)
        async with message.channel.typing():
            if message.attachments:
                for attachment in message.attachments:
                    print(f"{message.author.name} : ATTACHMENT + {cleaned_text}")
                    if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                        print("Processing Image")
                        await message.add_reaction('🖼️')
                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                if resp.status != 200:
                                    await message.channel.send('Unable to download the image.')
                                    return
                                image_data = await resp.read()
                                response_data = await generate_response_with_image_and_text(image_data, cleaned_text)
                                if response_data['error']:
                                    await message.channel.send(response_data['message'])
                                    await message.delete()
                                else:
                                    await split_and_send_messages(message, response_data['message'], 1700)
                                return
                    elif any(attachment.filename.lower().endswith(ext) for ext in ['.mp3', '.wav', '.aac', '.flac', '.ogg']):
                        await message.add_reaction('❌')
                        await message.add_reaction('🎵')
                        await message.channel.send("⚠️ Unfortunately, I can't hear audio files, but I can help you with decoding any legal gibberish in images and documents!")
                        return
                    elif any(attachment.filename.lower().endswith(ext) for ext in ['.mp4', '.mov', '.avi', '.mkv', '.flv']):
                        await message.add_reaction('❌')
                        await message.add_reaction('🎥')
                        await message.channel.send("⚠️ Unfortunately, I can't watch videos, but I can help you with decoding any legal gibberish in images and documents!")
                        return
                    elif any(attachment.filename.lower().endswith(ext) for ext in ['.pdf', '.txt']):
                        await process_attachments(message, cleaned_text)
                    else:
                        await message.add_reaction('❌')
                        await message.channel.send("⚠️ Unfortunately, this file is not supported, but I can help you with decoding any legal gibberish in images and other documents!")
                        return
            else:
                print(f"{message.author.name} : {cleaned_text}")
                if extract_url(cleaned_text) is not None:
                    await message.add_reaction('🔗')
                    print(f"Got URL: {extract_url(cleaned_text)}")
                    response_text = await process_url(cleaned_text)
                    await split_and_send_messages(message, response_text, 1700)
                    return
                if MAX_HISTORY == 0:
                    response_data = await generate_response_with_text(cleaned_text)
                    if response_data['error']:
                        await message.channel.send(response_data['message'])
                        await message.delete()
                    else:
                        await split_and_send_messages(message, response_data['message'], 1700)
                    return
                update_message_history(message.author.id, cleaned_text)
                response_data = await generate_response_with_text(get_formatted_message_history(message.author.id))
                if response_data['error']:
                    await message.channel.send(response_data['message'])
                    await message.delete()
                else:
                    update_message_history(message.author.id, response_data['message'])
                    await split_and_send_messages(message, response_data['message'], 1700)

#---------------------------------------------AI Generation History-------------------------------------------------

async def generate_response_with_text(message_text):
    try:
        prompt_parts = [message_text]
        response = gemini_model.generate_content(prompt_parts)
        if response._error:
            return {"error": True, "message": "🚫 Your message violates Simplify Me's [terms of service](https://simplify-me.com/terms-of-service/). If you believe this is an error, please contact an <@&1255420836811112602>."}
        return {"error": False, "message": response.text}
    except Exception as e:
        return {"error": True, "message": "🚫 Your message violates Simplify Me's [terms of service](https://simplify-me.com/terms-of-service/). If you believe this is an error, please contact an <@&1255420836811112602>."}

async def generate_response_with_image_and_text(image_data, text):
    try:
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
        prompt_parts = [image_parts[0], f"\n{text if text else 'What is this a picture of?'}"]
        response = gemini_model.generate_content(prompt_parts)
        if response._error:
            return {"error": True, "message": "🚫 Your message violates Simplify Me's [terms of service](https://simplify-me.com/terms-of-service/). If you believe this is an error, please contact an <@&1255420836811112602>."}
        return {"error": False, "message": response.text}
    except Exception as e:
        return {"error": True, "message": "🚫 Your message violates Simplify Me's [terms of service](https://simplify-me.com/terms-of-service/). If you believe this is an error, please contact an <@&1255420836811112602>."}

#---------------------------------------------Message History-------------------------------------------------

def update_message_history(user_id, new_message):
    if user_id not in message_history:
        message_history[user_id] = []

    message_history[user_id].append(new_message)

    if len(message_history[user_id]) > MAX_HISTORY:
        message_history[user_id].pop(0)

def get_formatted_message_history(user_id):
    if user_id in message_history:
        return '\n\n'.join(message_history[user_id])
    else:
        return "No messages found for this user."

#---------------------------------------------Sending Messages-------------------------------------------------

async def split_and_send_messages(message_system, text, max_length):
    messages = []
    for i in range(0, len(text), max_length):
        sub_message = text[i:i+max_length]
        messages.append(sub_message)

    for string in messages:
        await message_system.reply(string)

def clean_discord_message(text):
    return re.sub(r'<@[!&]?\d+>|<@\d+>', '', text).strip()

#---------------------------------------------Scraping Text from URL-------------------------------------------------

async def process_attachments(message, prompt):
    if prompt == "":
        prompt = SUMMERIZE_PROMPT  
    for attachment in message.attachments:
        await message.add_reaction('📄')
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status != 200:
                    await message.channel.send('Unable to download the attachment.')
                    return
                try:
                    text_data = await resp.text()
                    response_data = await generate_response_with_text(prompt + ": " + text_data)
                    if response_data['error']:
                        await message.channel.send(response_data['message'])
                    else:
                        await split_and_send_messages(message, response_data['message'], 1700)
                except Exception as e:
                    await message.channel.send("⚠️ An error occurred while processing the file.")
                return

#---------------------------------------------PDF and Text Processing Attachments-------------------------------------------------

async def process_pdf(pdf_data,prompt):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    pdf_document.close()
    print(text)
    return await generate_response_with_text(prompt+ ": " + text)

def extract_url(text):
    url_pattern = re.compile(r'(https?://\S+)')
    url_match = url_pattern.search(text)
    if url_match:
        return url_match.group(0)
    return None

async def process_url(text):
    url = extract_url(text)
    if url:
        response_data = await fetch_and_summarize_url(url)
        if response_data['error']:
            return response_data['message']
        else:
            return response_data['message']
    return "No summary available"

async def fetch_and_summarize_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            page_text = ' '.join([p.get_text() for p in soup.find_all('p')])
            return await generate_response_with_text(SUMMERIZE_PROMPT + page_text)

#---------------------------------------------Run Bot-------------------------------------------------
bot.run(DISCORD_BOT_TOKEN)
