from ollama import AsyncClient

class AgentService:

    def __init__(self, model: str = "llama3.2:1b", system_prompt: str | None = None):
        self._client = AsyncClient()
        self._history: list[dict[str, str]] = []
        self.model = model

        if system_prompt and not self._history:
            self._history.append(
                {
                    "role" : "system",
                    "content" : system_prompt
                }
            )


    async def response(self, prompt: str) -> str:
        
        self._history.append(
            {
                "role" : "user",
                "content" : prompt
            }
        )

        raw_response = await self._client.chat(
            model=self.model,
            messages=self._history
        )

        content = raw_response.message.content

        self._history.append(
            {
                "role" : "assistant",
                "content" : content

            }
        )

        return content

    def clear_history (self) -> None:
        self._history.clear()