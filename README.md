# Initial Template
- tag, repository_name, problem_description, problem_solution, new_information

# MCP
- search_memory(query:string)
- save_memory(data: JSON)

# Sample Architecture

Copilot ->(Search memory) -> MCP -> (Embedding) -> (Query) -> Chroma DB
Chroma DB -> (embedding) -> JSON -> MCP -> (Markdown | JSON) -> Copilot

- Thought: Instead of us manually creating skill and prompting copilot to save new informations learned, we can create a bg schedule task, which will scan our chat history, re-prompts the copilot/other agents in background and automatically stores new information.