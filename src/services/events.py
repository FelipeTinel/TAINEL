from agent_service import AgentService

class EventService:

    def __init__(self, system_prompt: str | None = None):
        self.agent = AgentService(system_prompt)

    def gen_unnecessary_comment():
        pass
