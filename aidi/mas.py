"""Implementation of a Large Language Model powered Multi-Agent System (MAS).

This module is used for handling tasks that involve natural language
processing and translation of source data models to target data models
using LLMs.
"""

import logging
from enum import Enum
from types import SimpleNamespace

import instructor
from autogen import (
    Agent,
    AssistantAgent,
    ChatResult,
    GroupChat,
    GroupChatManager,
    UserProxyAgent,
)
from autogen.cache import Cache
from autogen.coding import LocalCommandLineCodeExecutor
from openai import OpenAI
from pydantic import BaseModel, Field
from rich import print as print

from aidi.config import LoadConfig
from aidi.validation import validate_data_against_schema

# start logger
logger = logging.getLogger(__name__)


class ValidationStatus(str, Enum):
    """Class for Validation Status.

    Args:
        str (_type_): _description_
        Enum (_type_): _description_
    """

    INVALID = "INVALID"
    VALID = "VALID"


class ValidatorOutput(BaseModel):
    """Class for Validation Output.

    Args:
        BaseModel (_type_): Pydantic BaseModel
    """

    explanation: str = Field(
        ...,
        description="Explanation of the validation results.",
    )
    code_status: ValidationStatus = Field(
        ...,
        description="Status indicating whether validation process creation was VALID or INVALID.",  # noqa: E501
    )


class Task(BaseModel):
    """Class representing a single task in a task plan."""

    id: int = Field(..., description="Unique id of the task")
    task: str = Field(
        ...,
        description="""Contains the task in text form. If there are multiple tasks,
        this task can only be executed when all dependant subtasks have been answered.""",  # noqa: E501
    )
    subtasks: list[int] = Field(
        default_factory=list,
        description="""List of the IDs of subtasks that need to be answered before
        we can answer the main question. Use a subtask when anything may be unknown
        and we need to ask multiple questions to get the answer.
        Dependencies must only be other tasks.""",  # noqa: E501
    )


class TaskPlan(BaseModel):
    """Container class representing a tree of tasks and subtasks."""

    task_graph: list[Task] = Field(
        ...,
        description="List of tasks and subtasks that need to be done to complete the main task. Consists of the main task and its dependencies.",  # noqa: E501
    )


## need to rebuild recursive generic models (Pydantic)
Task.model_rebuild()
TaskPlan.model_rebuild()


class CustomLLMClient:
    """Class to create custom client in Autogen."""

    def __init__(self, config, response_model, service_settings):
        """CustomLLMClient init."""
        self.response_model = (
            response_model  # Store the model type dynamically
        )
        self.model = service_settings["selected_model"]
        self.LLM_SERVICE = service_settings["service_name"]
        if self.LLM_SERVICE == "ollama":
            self.BASE_URL_OLLAMA_COMPATIBLE_WITH_OPENAI_API = service_settings[
                "base_url_compatible_with_openai_api"
            ]

    def create(self, params) -> SimpleNamespace:
        """Create CustomLLMClient."""
        if self.LLM_SERVICE == "OpenAI":
            client = instructor.from_openai(OpenAI())
        elif self.LLM_SERVICE == "ollama":
            client = instructor.from_openai(
                OpenAI(
                    base_url=self.BASE_URL_OLLAMA_COMPATIBLE_WITH_OPENAI_API,
                    api_key="ollama",  # required, but unused
                ),
                mode=instructor.Mode.JSON,
            )
        else:
            raise ValueError("Invalid LLM service name.")

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=params["messages"],
                response_model=self.response_model,
                temperature=0,
                max_retries=5,
            )
        except Exception as e:
            print("ERROR:", e)
            raise

        autogen_response = SimpleNamespace()
        autogen_response.choices = []
        autogen_response.model = "custom_llm_json"

        choice = SimpleNamespace()
        choice.message = SimpleNamespace()
        # Dynamically serialize the response using the selected response model
        choice.message.content = response.model_dump_json()
        choice.message.function_call = None
        autogen_response.choices.append(choice)
        return autogen_response

    def message_retrieval(self, response):
        """Message retrieval."""
        choices = response.choices
        return [choice.message.content for choice in choices]

    def cost(self, response) -> float:
        """Cost."""
        response.cost = 0
        return 0

    @staticmethod
    def get_usage(response):
        """Get Usage."""
        return {}


class MultiAgentSystem:
    """Class to create and run an LLM multi agent system."""

    def __init__(self, service_settings, full_config):
        """Init MultiAgentSystem."""
        self.config_list = service_settings.get("config_list")
        self.custom_config_list = service_settings.get("custom_config_list")
        self.service_settings = service_settings
        self.full_config = full_config
        self.Selected_Tool = (
            validate_data_against_schema  # function to be called by the agent
        )
        self.Name_Selected_Tool = str(self.Selected_Tool.__name__)

        logger.info("Initializing Multi Agent System.")

    def create_and_run(self, task) -> ChatResult:
        """Creates and runs a set of agents."""
        logger.info("Executing MultiAgentSystem create_and_run function.")

        if self.full_config["group_chat"].get("structured_output"):
            # Create planner agent.
            planner = AssistantAgent(
                name="Planner",
                system_message=self.full_config["prompt"].get(
                    "planner_system_message"
                ),
                llm_config={
                    "config_list": self.custom_config_list,
                    "cache": None,
                    "cache_seed": None,
                },
            )

            planner.register_model_client(
                model_client_cls=CustomLLMClient,
                response_model=TaskPlan,
                service_settings=self.service_settings,
            )
        else:
            # Create planner agent without custom config.
            planner = AssistantAgent(
                name="Planner",
                system_message=self.full_config["prompt"].get(
                    "planner_system_message"
                ),
                llm_config={
                    "config_list": self.config_list,
                    "cache": None,
                    "cache_seed": None,
                },
            )

        user_proxy = UserProxyAgent(
            name="Admin",
            system_message=self.full_config["prompt"].get(
                "user_proxy_system_message"
            ),
            code_execution_config=False,
        )

        coder = AssistantAgent(
            name="Coder",
            llm_config={
                "config_list": self.config_list,
                "cache": None,
                "cache_seed": None,
            },
            system_message=self.full_config["prompt"].get(
                "coder_system_message"
            ),
        )
        if self.full_config["group_chat"].get("structured_output"):
            validator = AssistantAgent(
                name="Validator",
                llm_config={
                    "config_list": self.custom_config_list,
                    "cache": None,
                    "cache_seed": None,
                },
                system_message=self.full_config["prompt"].get(
                    "validator_system_message"
                ),
            )

            validator.register_model_client(
                model_client_cls=CustomLLMClient,
                response_model=ValidatorOutput,
                service_settings=self.service_settings,
            )
        else:
            # Create validator agent without custom config.
            validator = AssistantAgent(
                name="Validator",
                llm_config={
                    "config_list": self.config_list,
                    "cache": None,
                    "cache_seed": None,
                },
                system_message=self.full_config["prompt"].get(
                    "validator_system_message"
                ),
            )

        code_executor = UserProxyAgent(
            name="Executor",
            system_message=self.full_config["prompt"].get(
                "executer_system_message"
            ),
            human_input_mode="NEVER",  ### "ALWAYS"
            code_execution_config={
                "last_n_messages": 3,
                "executor": LocalCommandLineCodeExecutor(
                    work_dir=self.full_config["code"].get(
                        "code_folder", "translation_folder"
                    ),
                    timeout=60,
                ),
            },
        )
        ## overrite validator settings if validation_by_tool is True
        if self.full_config["group_chat"].get("validation_by_tool"):
            validator = AssistantAgent(
                name="Validator",
                llm_config={
                    "config_list": self.config_list,
                    "cache": None,
                    "cache_seed": None,
                },
                system_message=self.full_config["prompt"].get(
                    "tool_calling_validator_system_message"
                ),
            )

            tool_runner_agent = AssistantAgent(
                name="function_executor_agent",
                system_message=self.full_config["prompt"].get(
                    "tool_runner_system_message"
                ),
                llm_config={
                    "config_list": self.config_list,
                    "cache": None,
                    "cache_seed": None,
                },
            )

            # Register the tool signature with the assistant agent.
            validator.register_for_llm(
                name=self.Name_Selected_Tool, description="Data Validator"
            )(self.Selected_Tool)
            # Register the tool function with the user proxy agent.
            tool_runner_agent.register_for_execution(
                name=self.Name_Selected_Tool
            )(self.Selected_Tool)

        def _custom_speaker_selection_func(
            last_speaker: Agent, groupchat: GroupChat
        ):
            """Define a customized speaker selection function.

            A recommended way is to define a transition for each speaker
            in the groupchat.

            Returns:
                Return an `Agent` class or a string from ['auto', 'manual',
                'random', 'round_robin'] to select a default method to use.
            """
            messages = groupchat.messages

            if len(messages) <= 1:
                # first, let the Coder retrieve relevant data
                return planner

            if last_speaker is planner:
                # if the last message is from planner,
                # let the Coder to write code
                return coder

            elif last_speaker is coder:
                if (
                    "```python" in messages[-1]["content"]
                    or "python_code" in messages[-1]["content"]
                    or "Python" in messages[-1]["content"]
                ):
                    return code_executor
                else:
                    # Otherwise, let the user_proxy to continue
                    return user_proxy
            elif last_speaker is code_executor:
                if "exitcode: 1" in messages[-1]["content"]:
                    # If the last message indicates an error,
                    # let the coder to improve the code
                    return coder
                else:
                    return validator

            elif last_speaker is validator:
                # If the last message indicates an error, go to X agent again
                if "INVALID" in messages[-1]["content"]:
                    return planner  ##coder #planner
                elif messages[-1].get("tool_calls"):
                    return tool_runner_agent
                else:
                    # Otherwise, go to the user
                    return user_proxy  ## return None
            elif self.full_config["group_chat"].get("validation_by_tool") and (
                last_speaker is tool_runner_agent
            ):
                return validator  ##
            else:
                # default to auto speaker selection method
                return "auto"

        if self.full_config["group_chat"].get("validation_by_tool"):
            active_agent_list = [
                user_proxy,
                coder,
                validator,
                code_executor,
                planner,
                tool_runner_agent,
            ]
        else:
            active_agent_list = [
                user_proxy,
                coder,
                validator,
                code_executor,
                planner,
            ]

        groupchat = GroupChat(
            agents=active_agent_list,
            messages=self.full_config["group_chat"].get("messages"),
            max_round=self.full_config["group_chat"].get("max_round"),
            speaker_selection_method=_custom_speaker_selection_func,
            send_introductions=self.full_config["group_chat"].get(
                "send_introductions"
            ),
        )

        manager = GroupChatManager(
            groupchat=groupchat,
            llm_config={"config_list": self.config_list, "cache_seed": None},
        )

        is_cache = self.full_config["group_chat"].get("cache_chat")
        if is_cache:
            with Cache.disk(cache_seed=45) as cache:
                logger.info("Initiating group chat with cache.")
                groupchat_history_custom = user_proxy.initiate_chat(
                    manager,
                    message=task,
                    cache=cache,
                )
        else:
            logger.info("Initiating group chat without cache.")
            groupchat_history_custom = user_proxy.initiate_chat(
                manager,
                message=task,
            )
        return groupchat_history_custom


# Execute main if script is run directly for testing purposes
if __name__ == "__main__":
    task1 = """
    The task is to create a python code that translate from  source data model to target data model.

    An example of source and target data structures are below:
    source model example in json format:
        {
            "Category":"CV-CV-Abutment-G-P",
            "ss_epd_id":"9cf0bb8930ab4d3a9e8082b475796fae",
        }
    target model example translated from the example of source data model in json format:
        {
            "Name_notes":"CV-CV-Abutment-G-P",
            "Asset_Code":"9cf0bb8930ab4d3a9e8082b475796fae",
        }
    another example:
    source model example in json format:
    source data model:
        {
            "Category":"CV-CV-Barrier-G-P",
            "QTY":110,
            "ss_epd_id":"5e99ea4bf1124b66a0899c4e072550f4",
        }
    target model example translated from the example of source data model in json format:
        {
            "Name_notes":"CV-CV-Barrier-G-P",
            "Asset_Code":"5e99ea4bf1124b66a0899c4e072550f4",
        }

    Here is the source model to be translated:
        {
            "Category":"CV-CV-Abutment-G-P",
            "ss_epd_id":"9cf0bb8930ab4d3a9e8082b475796fae",
        }
    Here is the target schema:
    {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "Name_notes": {
        "type": "string",
        "description": "Notes or classification for the asset name."
        },
        "Asset_Code": {
        "type": "string",
        "description": "Unique identifier code for the asset."
        },
    },
    "required": ["Name_notes", "Asset_Code"],
    "additionalProperties": false
    }
    """  # noqa: E501
    # load configuration
    (
        config_list,
        custom_config_list,
        service_settings,
        log_config,
        full_config,
    ) = LoadConfig().get_configuration()
    # create and run MAS
    mas = MultiAgentSystem(service_settings, full_config)
    groupchat_history_custom = mas.create_and_run(task1)
    # print(Pretty(groupchat_history_custom))
