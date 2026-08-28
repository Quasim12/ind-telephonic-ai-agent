from dotenv import load_dotenv

from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession, JobContext
from livekit.plugins import google


load_dotenv(".env")


server = AgentServer()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful and natural voice AI assistant. "

                "Have a fast, natural and conversational phone conversation. "

                "The caller may speak English, Hindi, or Hinglish. "
                "Understand Indian English accents and Hindi spoken by Indian callers. "

                "Respond in the same language used by the caller. "
                "If the caller speaks Hinglish, respond naturally in Hinglish. "

                "Keep your answers short and conversational. "
                "Do not give unnecessarily long answers. "

                "Respond immediately when the caller finishes speaking. "
                "Do not wait unnecessarily before answering. "

                "If the caller interrupts you, stop speaking and listen to them. "
                "Do not continue your previous response after an interruption."
            )
        )


@server.rtc_session(agent_name="telephonic-agent")
async def entrypoint(ctx: JobContext):

    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            model="gemini-2.5-flash-native-audio-preview-12-2025",
            voice="Puck",

            # Keep Gemini's native realtime VAD enabled.
            # Do NOT disable automatic activity detection.

            thinking_config=None,
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )

    await session.generate_reply(
        instructions=(
            "Greet the caller naturally and briefly. "
            "Say hello and ask how you can help them today. "
            "Do not give a long introduction."
        )
    )


if __name__ == "__main__":
    agents.cli.run_app(server)