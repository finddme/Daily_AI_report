from model.models import LLM_Definition

llm_df = LLM_Definition()

llm_map={"openai":llm_df.openai_llm(),
        "claude":llm_df.claude_llm(),
        }