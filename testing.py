from forgeX.core.engine.graph import builder

query = """
hey like the website which is built with html,css and js the theme is not good like make it something aura and glowing

"""

workspace_dir = r"C:\Users\DVS\OneDrive\Desktop\hackerrank\test_agent_workspace"

if __name__ == "__main__":
    result = builder.invoke(
        {
            "user_query": query,
            "workspace": workspace_dir,
        },
        config={"configurable": {"thread_id": "2"}},
    )
    print(result)
