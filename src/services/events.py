import asyncio
import random
from config.prompts import UNNECESSARY_COMMENT
from typing import Callable, Awaitable
from agent_service import AgentService

class EventManager:
    def __init__(
        self, 
        agent: AgentService, 
        on_comment_callback: Callable[[str], Awaitable[None]],
        min_interval: int = 30, 
        max_interval: int = 120
    ):
        self.agent = agent
        self.on_comment_callback = on_comment_callback
        self.min_interval = min_interval
        self.max_interval = max_interval
        self._running = False
        self._task: asyncio.Task | None = None
        self.event_prompts = UNNECESSARY_COMMENT

    async def _event_loop(self):
        while self._running:
            wait_time = random.randint(self.min_interval, self.max_interval)
            await asyncio.sleep(wait_time)

            if not self._running:
                break

            random_prompt = random.choice(self.event_prompts)
            
            try:
                comment = await self.agent.response(f"[EVENTO INTERNO ESPONTÂNEO]: {random_prompt}")

                await self.on_comment_callback(comment)
            except Exception as e:
                print(f"Erro ao gerar evento espontâneo: {e}")

    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._event_loop())

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()