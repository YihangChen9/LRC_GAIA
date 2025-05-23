from dotenv import load_dotenv
load_dotenv()

from camel.models import ModelFactory
from camel.toolkits import (
    SearchToolkit,
    WebToolkit,
)
from camel.types import ModelPlatformType, ModelType

from utils import OwlRolePlaying, run_society


def construct_society(question: str) -> OwlRolePlaying:
    r"""Construct a society of agents based on the given question.
    
    Args:
        question (str): The task or question to be addressed by the society.
        
    Returns:
        OwlRolePlaying: A configured society of agents ready to address the question.
    """
    
    # Create models for different components
    models = {
        "user": ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict={"temperature": 0},
        ),
        "assistant": ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict={"temperature": 0},
        ),
        "web": ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict={"temperature": 0},
        ),
        "planning": ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict={"temperature": 0},
        ),
        "search": ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict={"temperature": 0},
        ),
    }
    
    # Configure toolkits
    tools = [
        *WebToolkit(
            headless=False,  # Set to True for headless mode (e.g., on remote servers)
            web_agent_model=models["web"],
            planning_agent_model=models["planning"],
        ).get_tools(),
        *SearchToolkit(model=models["search"]).get_tools(),
    ]
    
    # Configure agent roles and parameters
    user_agent_kwargs = {"model": models["user"]}
    assistant_agent_kwargs = {"model": models["assistant"], "tools": tools}
    
    # Configure task parameters
    task_kwargs = {
        "task_prompt": question,
        "with_task_specify": False,
    }
    
    # Create and return the society
    society = OwlRolePlaying(
        **task_kwargs,
        user_role_name="user",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="assistant",
        assistant_agent_kwargs=assistant_agent_kwargs,
    )
    
    return society


def main():
    r"""Main function to run the OWL system with an example question."""
    # Example research question
    question = (
        "What was the volume in m^3 of the fish bag that was calculated in "
        "the University of Leicester paper `Can Hiccup Supply Enough Fish "
        "to Maintain a Dragon's Diet?`"
    )
    
    # Construct and run the society
    society = construct_society(question)
    answer, chat_history, token_count = run_society(society)
    
    # Output the result
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
