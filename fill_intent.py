import json
import os

from environs import Env
from google.cloud import dialogflow

BASE_DIR = os.path.dirname(__file__) or '.'
INTENTS_JSON_PATH = os.path.join(BASE_DIR, "intents", "questions.json")


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases,
        messages=[message]
    )

    intents_client.create_intent(request={"parent": parent, "intent": intent})


def main():
    env = Env()
    env.read_env()
    google_project_id = env("GOOGLE_PROJECT_ID")
    with open(INTENTS_JSON_PATH, "r", encoding="utf-8") as intents_json:
        intents = json.load(intents_json)

    for display_name, intent in intents.items():
        training_phrases_parts = intent.get("questions")
        message_texts = [intent.get("answer")]
        create_intent(google_project_id, display_name, training_phrases_parts,
                      message_texts)


if __name__ == "__main__":
    main()
