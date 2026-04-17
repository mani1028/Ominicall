import asyncio
# Now importing is easy because we fixed the folder names!
from sdk_core.python_app.core import OmniCallApp

async def main():
    # A developer only needs these 2 lines!
    app = OmniCallApp(user_id="UserB")
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())