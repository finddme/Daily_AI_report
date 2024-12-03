from model.models import LLM_Definition

llm_df = LLM_Definition()

llm_map={"together":llm_df.together_llm(),
        "claude":llm_df.claude_llm(),
        }