import re
from ollama import AsyncClient

class AgentService:

    def __init__(self, model: str = "llama3.2:1b", system_prompt: str | None = None):
        self._client = AsyncClient()
        self._history: list[dict[str, str]] = []
        self._system_prompt = system_prompt
        self.model = model
        self._init_history()

    def _init_history(self) -> None:
        if self._system_prompt:
            self._history.append({"role": "system", "content": self._system_prompt})

    def _sanitize_input(self, text: str) -> str:
        cleaned = re.sub(r'\[\s*(SYSTEM|INSTRUCTION|PROMPT)\s*\]', '', text, flags=re.IGNORECASE)
        cleaned = re.sub(r'<\/?\s*(system|instruction)\s*>', '', cleaned, flags=re.IGNORECASE)
        return cleaned.strip()
    
    async def response(self, prompt: str) -> str:

        clean_prompt = self._sanitize_input(prompt)

        wrapped_user_content = (
            f"[ENTRADA DO USUÁRIO]: {clean_prompt}\n"
            "[RELEMBRETE]: Responda estritamente mantendo a personalidade do TAINEL DROID AI, em 3ª pessoa."
        )
        
        self._history.append(
            {
                "role" : "user",
                "content" : wrapped_user_content
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
        self._init_history()