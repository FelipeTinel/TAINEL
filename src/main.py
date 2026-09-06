import sys
import asyncio
from PyQt6.QtWidgets import QApplication
import qasync

from config.prompts import SYSTEM_PROMPT
from services.agent_service import AgentService
from services.events import EventManager
from services.widget import MascotWidget


async def main():
    app = QApplication(sys.argv)

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    agent = AgentService(
        model="llama3.2:1b",
        system_prompt=SYSTEM_PROMPT
    )

    widget = MascotWidget(agent=agent)
    widget.show()

    async def handle_spontaneous_comment(text: str):
        widget.set_speech(text)

    event_system = EventManager(
        agent=agent,
        on_comment_callback=handle_spontaneous_comment,
        min_interval=15,
        max_interval=30
    )
    event_system.start()

    with loop:
        await loop.run_forever()


if __name__ == "__main__":
    asyncio.run(main())