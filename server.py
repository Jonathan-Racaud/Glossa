import os
from mcp.server.fastmcp  import FastMCP
from constants import *
from flashcards.tools import flashcards_tools
from lessons.tools import lessons_tools

mcp = FastMCP("StatefulServer")

if not os.path.exists(FLASHCARDS_DIR):
    os.makedirs(FLASHCARDS_DIR)

if not os.path.exists(LESSONS_DIR):
    os.makedirs(LESSONS_DIR)

for tool in flashcards_tools:
    mcp.add_tool(tool)

for tool in lessons_tools:
    mcp.add_tool(tool)

mcp.run(transport="streamable-http")
