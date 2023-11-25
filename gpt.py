import os
import time
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
THREAD_ID = os.getenv("THREAD_ID")

client = OpenAI(api_key=API_KEY)

async def generate_response(prompt):
	message = client.beta.threads.messages.create(
		thread_id = THREAD_ID,
		role = "user",
		content = prompt
	)

	run = client.beta.threads.runs.create(
		thread_id = THREAD_ID,
		assistant_id = ASSISTANT_ID
	)

	run = client.beta.threads.runs.retrieve(
		thread_id = THREAD_ID,
		run_id = run.id
	)

	while run.status == "in_progress":
		time.sleep(2)
		run = client.beta.threads.runs.retrieve(
			thread_id = THREAD_ID,
			run_id = run.id
		)
		print(run.status)

	messages = client.beta.threads.messages.list(
		thread_id= THREAD_ID
	)

	return messages.data[0].content[0].text.value
