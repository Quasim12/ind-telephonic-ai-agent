import asyncio
import os
import uuid
import traceback

from dotenv import load_dotenv
from livekit import api


# Load environment variables
load_dotenv(".env")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AGENT_NAME = "telephonic-agent"
TRUNK_ID = "ST_pgKWKvMrLWDN"
PHONE_NUMBER = "+917783807356"


async def main():
    # -----------------------------------------------------------------------
    # Check environment variables
    # -----------------------------------------------------------------------

    livekit_url = os.getenv("LIVEKIT_URL")
    livekit_api_key = os.getenv("LIVEKIT_API_KEY")
    livekit_api_secret = os.getenv("LIVEKIT_API_SECRET")

    if not livekit_url:
        print("ERROR: LIVEKIT_URL is missing in .env")
        return

    if not livekit_api_key:
        print("ERROR: LIVEKIT_API_KEY is missing in .env")
        return

    if not livekit_api_secret:
        print("ERROR: LIVEKIT_API_SECRET is missing in .env")
        return

    # -----------------------------------------------------------------------
    # Create LiveKit API client
    # -----------------------------------------------------------------------

    livekit_api = api.LiveKitAPI(
        url=livekit_url,
        api_key=livekit_api_key,
        api_secret=livekit_api_secret,
    )

    # Create unique room name
    room_name = f"outbound-{uuid.uuid4().hex[:8]}"

    try:
        print("=" * 60)
        print("Starting outbound call")
        print("=" * 60)

        print(f"Room       : {room_name}")
        print(f"Agent      : {AGENT_NAME}")
        print(f"Trunk ID   : {TRUNK_ID}")
        print(f"Phone      : {PHONE_NUMBER}")
        print("=" * 60)

        # -------------------------------------------------------------------
        # Step 1: Dispatch AI agent
        # -------------------------------------------------------------------

        print("\n[1/2] Dispatching AI agent...")

        await livekit_api.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name=AGENT_NAME,
                room=room_name,
                metadata=PHONE_NUMBER,
            )
        )

        print("Agent dispatched successfully.")
        print(f"Agent: {AGENT_NAME}")
        print(f"Room : {room_name}")

        # -------------------------------------------------------------------
        # Step 2: Create outbound SIP participant
        # -------------------------------------------------------------------

        print("\n[2/2] Starting outbound SIP call...")
        print(f"Calling: {PHONE_NUMBER}")

        participant = await livekit_api.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                sip_trunk_id=TRUNK_ID,
                sip_call_to=PHONE_NUMBER,
                room_name=room_name,
                participant_identity="phone_user",
                participant_name="Phone User",
                wait_until_answered=True,
            )
        )

        # -------------------------------------------------------------------
        # Success
        # -------------------------------------------------------------------

        print("\n" + "=" * 60)
        print("CALL ANSWERED SUCCESSFULLY")
        print("=" * 60)

        print(f"Room        : {room_name}")
        print(f"Participant : {participant}")
        print("=" * 60)

    except Exception as e:
        # -------------------------------------------------------------------
        # Error
        # -------------------------------------------------------------------

        print("\n" + "=" * 60)
        print("CALL FAILED")
        print("=" * 60)

        print(f"Error type    : {type(e).__name__}")
        print(f"Error message : {e}")

        print("\nFull traceback:")
        traceback.print_exc()

        print("=" * 60)

    finally:
        # -------------------------------------------------------------------
        # Close LiveKit API connection
        # -------------------------------------------------------------------

        await livekit_api.aclose()


if __name__ == "__main__":
    asyncio.run(main())