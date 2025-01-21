# Configuration Guide

The `config_aidi.yaml` file is a critical configuration file for the AIDI Tool. This guide will help you understand and customize the configuration based on your specific needs.

## Configuration Sections

### Logging Configuration

This section defines the logging settings for the AIDI Tool.

```yaml
logging:
  level: "INFO"
  log_file_name: "./translation_log.log"
```

- `level`: The logging level (e.g., INFO, DEBUG).
- `log_file_name`: The file where logs will be stored.

### Data Configuration

This section specifies the paths to the data folders.

```yaml
data:
  data_folder: "./data/data1/"
```

- `data_folder`: The folder where the data is stored.

### Code Configuration

This section specifies the folder where the generated code will be saved.

```yaml
code:
  code_folder: "./translation_folder/"
```

- `code_folder`: The folder where the generated code will be saved.

### Active Service

This section specifies the active service to be used by the AIDI Tool.

```yaml
# active_service:
# active_service: "ollama" # "ollama"
active_service: "OpenAI"
```

- `active_service`: The active service to be used (e.g., OpenAI, ollama).

### Services Configuration

This section defines the configuration for different services.

#### OpenAI Service

```yaml
services:
  OpenAI:
    service_name: "OpenAI"
    model: &openai_model "gpt-4o-2024-08-06"
    embedding: "text-embedding-3-small"
    api_key: &key "YOUR_OPENAI_API_KEY"
    selected_model: *openai_model
    config_list:
      - model: *openai_model
        api_key: *key
    custom_config_list:
      - model: "custom_llm_json"
        model_client_cls: "CustomLLMClient"
```

- `service_name`: The name of the service.
- `model`: The model to be used.
- `embedding`: The embedding model.
- `api_key`: The API key for the service.
- `selected_model`: The selected model.
- `config_list`: A list of configurations for the service.
- `custom_config_list`: A list of custom configurations for the service.

#### Ollama Service

```yaml
  ollama:
    service_name: "ollama"
    base_url: "http://52.56.167.144:11434/"
    base_url_compatible_with_openai_api: "http://52.56.167.144:11434/v1/"
    model: &ollama_model "mistral-nemo"
    selected_model: *ollama_model
    embedding: "all-minilm"
    config_list:
      - model: *ollama_model
        base_url: "http://52.56.167.144:11434/v1/"
        api_type: "open_ai"
        api_key: "ollama"
        price: [0, 0]
    custom_config_list:
      - model: "custom_llm_json"
        model_client_cls: "CustomLLMClient"
```

- `service_name`: The name of the service.
- `base_url`: The base URL for the service.
- `base_url_compatible_with_openai_api`: The base URL compatible with OpenAI API.
- `model`: The model to be used.
- `selected_model`: The selected model.
- `embedding`: The embedding model.
- `config_list`: A list of configurations for the service.
- `custom_config_list`: A list of custom configurations for the service.

### Prompt Configuration

This section defines the components and template for the task prompt.

```yaml
prompt:
  prompt_components: ["sd","ts"]
  prompt_template: |
    Translate source data to target data according to the provided data, schema, and ontology information.

    Source Data Sample 1:
    {source_data_sample1}

    Target Data Sample 1:
    {target_data_sample1}

    Source Data Sample 2:
    {source_data_sample2}

    Target Data Sample 2:
    {target_data_sample2}

    Source Data Schema:
    {source_schema}

    Target Data Schema:
    {target_schema}

    Source Ontology:
    {source_ontology_sample}

    Target Ontology:
    {target_ontology_sample}

    Instructions:
    Translate fields in the source data to match the target data format, using both schema structures 
    and ontology mappings. Apply any necessary transformations as indicated by ontology relationships.
    
    Source Data to be translated:
    {source_data}
    
    Target Data:
    {target_data}
```

- `prompt_components`: The components to be added to the task prompt.
- `prompt_template`: The template for the task prompt.

### System Messages

This section defines various system messages for different agents.

```yaml
  planner_system_message: |
        You are a world class task planning algorithm capable of breaking apart tasks into dependant subtasks...
  user_proxy_system_message:
        - "A human admin. Give the task, and send instructions to perform a data translation."
  coder_system_message: |
        Python Code Writer. You will write python code...
  executor_system_message: "Executor. Execute the code written by the Coder and report the result."
  validator_system_message: |
        Validator. Please validate the 'Code output' of the executed code by the Executor against the target schema...
  tool_calling_validator_system_message: |
        Validator.You will assess if the generated target data is validated using the tools provided...
  tool_runner_system_message: |
        Tool runner. This agent runs all functions for the group...
```

- `planner_system_message`: Message for the planner agent.
- `user_proxy_system_message`: Message for the user proxy agent.
- `coder_system_message`: Message for the coder agent.
- `executor_system_message`: Message for the executor agent.
- `validator_system_message`: Message for the validator agent.
- `tool_calling_validator_system_message`: Message for the tool calling validator agent.
- `tool_runner_system_message`: Message for the tool runner agent.

### Group Chat Configuration

This section defines the configuration for group chat.

```yaml
group_chat:
  messages: []
  max_round: 50
  send_introductions: true
  cache_chat: false
  structured_output: true
  validation_by_tool: true
```

- `messages`: Initial messages for the group chat.
- `max_round`: Maximum number of rounds for the chat.
- `send_introductions`: Whether to send introductions.
- `cache_chat`: Whether to cache the chat.
- `structured_output`: Whether to use structured output.
- `validation_by_tool`: Whether to use validation by tool.

## Conclusion

This guide provides an overview of the `config_aidi.yaml` file. Customize the configuration based on your specific needs to ensure the AIDI Tool functions correctly. Ensure the `config_aidi.yaml` file is present in the current folder before executing the workflow.
