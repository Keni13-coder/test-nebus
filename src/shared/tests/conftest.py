import asyncio
import sys
from typing import Generator

import pytest


@pytest.fixture(scope="module")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for all async tests."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    
    yield loop
    
    # Cleanup
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.run_until_complete(loop.shutdown_default_executor())
    loop.close()
    asyncio.set_event_loop(None)