import os

from mcp.server.fastmcp  import FastMCP

from constants import *

if __name__ == "__main__":
    if not os.path.exists(FLASHCARDS_DIR):
        os.makedirs(FLASHCARDS_DIR)

    mcp = FastMCP("StatefulServer")
    mcp.run(transport="streamable-http")
