from google.cloud import dialogflow


async def detect_intent_texts(project_id: str,
                              session_id: str,
                              text: str,
                              language_code: str = "ru-RU",
                              social_network: str = "tg") -> str:
    """Returns the result of detect intent with texts as inputs."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text,
                                      language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if social_network != "vk" or not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text
