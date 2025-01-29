AIDI: AI Assistant for Data Interoperability
==============================================

The **AIDI Tool** is an effective solution for automating data translation tasks using a combination of schema validation, ontology mapping, and an LLM-powered multi-agent system. This tool enables seamless translation of source data into target formats while leveraging advanced AI techniques for accuracy and efficiency.

Features
--------

*   **Configuration Management**: Dynamically load configurations for data processing, logging, and multi-agent system operations.
    
*   **Data Ingestion**: Validate and load source/target data, schemas, and ontologies from structured files.
    
*   **Prompt Generation**: Automatically craft structured task prompts for LLMs based on the provided data.
    
*   **Multi-Agent System**: Utilize autonomous agents to execute translation tasks, with rich collaboration enabled by LLMs.
    
*   **Detailed Logging**: Track workflow progress and issues with configurable logging settings.
    

Workflow
--------

1.  **Load Configuration**Use the LoadConfig module to parse YAML configuration files for logging, data ingestion, and prompt settings.
    
2.  **Ingest Data**The TranslationDataIngest module handles loading and validating source and target data, schemas, and ontologies, ensuring a strong foundation for translation.
    
3.  **Generate Task Prompt**Leverage the ingested data to create a structured prompt for the multi-agent system, specifying the necessary components for translation.
    
4.  **Run Multi-Agent System**Deploy the MultiAgentSystem module to execute translation tasks using LLMs, with agents collaborating to achieve accurate mappings and transformations.
    
5.  **Log and Monitor**Monitor the workflow using detailed logs stored in a configurable log file.
    
Installation For Users
------------

### Prerequisites

Ensure you have the following installed:

*   Python 3.11 or later

*   (Optional) Virtual Environment:  Conda, Poetry, Venv



### Steps

1.  Download the aidi.zip file from the repo.
2.  List of commands to install
      ```bash
         tar -xvf aidi.zip
         cd aidi
      ``` 
      Optional:
      ```bash
         conda create --name env_aidi python=3.11
         conda activate env_aidi

      ``` 
      Install:
      ```bash
         pip install ./dist/aidi-0.1.0-py3-none-any.whl
      ``` 

      Run Command:
      ```bash
         aidi
      ``` 
3. For command help:
      ```bash
         aidi --help
      ``` 


Installation For Developers
------------

### Prerequisites

Ensure you have the following installed:

*   Python 3.11 or later
    
*   Poetry for dependency management
    

### Steps

1.  git clone https://github.com/CDECatapult/dsch-if-AIDI-tool

    
2.  Install dependencies using Poetry:
    ```bash
    poetry install
    ``` 
    
3.  Set up configuration files:
    
    *   Edit the YAML configuration files located in the config/ directory to suit your environment.
        
Code Quality Checks
-------------    
Tox runs linting, formatting, type checks and tests accross different python versions defined in pyproject.toml file.

   ```bash
   poetry run tox
   ``` 

Configuration
-------------

The tool uses YAML-based configuration files. Below are some key sections:

*   **Logging**: Define log levels (INFO, DEBUG, etc.) and file names for log storage.
    
*   **Data Settings**: Specify paths to source/target data, schemas, and ontologies.
    
*   **Prompt Settings**: Configure prompt templates and components for task generation.
    
*   **Service Settings**: Set up API keys and endpoints for LLM services.
    
Please read the Confguration Guide for more information about how to modify the configuration file (i.e., config_aidi.yaml).
    
## Data Folder

This folder contains the necessary files for source and target data, schemas, and ontologies used in data processing and transformation tasks.

### Data Files

1. **`source_data.json`**
   - Contains the complete source data set used for processing.
   
2. **`source_data_sample1.json`**
   - Sample file from the source data, used for testing or demonstration purposes.

3. **`source_data_sample2.json`**
   - Another sample file from the source data, showcasing a different subset.

4. **`source_ontology.ttl`**
   - Turtle file representing the ontology of the source data, including relationships and constraints.

5. **`source_schema.json`**
   - Schema definition for the source data, describing its structure and expected fields.

**Target Files**
1. **`target_data.json`**
   - Contains the complete target data set, which is the result of transformation from source data.

2. **`target_data_sample1.json`**
   - Sample file from the target data, used for testing or demonstration purposes.

3. **`target_data_sample2.json`**
   - Another sample file from the target data, showcasing a different subset.

4. **`target_ontology.ttl`**
   - Turtle file representing the ontology of the target data, including relationships and constraints.

5. **`target_schema.json`**
   - Schema definition for the target data, describing its structure and expected fields.

**Usage**
- **Source Files**: Used as inputs for transformation processes or validation against the source schema and ontology.
- **Target Files**: Represent outputs of the transformation process and are validated against the target schema and ontology.
- **Sample Files**: Sample data files.

 **Notes**
- Ensure schema files (`source_schema.json`, `target_schema.json`) are consistent with their respective data files.
- Validate ontologies (`source_ontology.ttl`, `target_ontology.ttl`) to confirm data relationships and constraints are correctly modeled.
- Sample files (`*_sample1.json`, `*_sample2.json`) are subsets of their respective full datasets and may not represent the complete data structure.

---

 **Folder Structure**
```
data/ 
├── source_data.json 
├── source_data_sample1.json 
├── source_data_sample2.json 
├── source_ontology.ttl 
├── source_schema.json 
├── target_data.json 
├── target_data_sample1.json 
├── target_data_sample2.json 
├── target_ontology.ttl 
├── target_schema.json 
```

### Workflow Execution
Make sure config_aidi.yaml file is in your current working 
#### Configuration File
The `config_aidi.yaml` file is a critical configuration file for this project. You can:

- Copy the template from the project repo directory 
- Customise the configuration based on your specific needs

Ensure the `config_aidi.yaml` file is present in the current folder before executing the workflow.

```bash
aidi
```  
or

from the project folder:
```bash
python -m aidi
```  

Logs will capture the start and end of the workflow, with detailed information about each stage.  

Modules
-------

### aidi.py

*   Entry point of the AIDI Tool.
    
*   Loads configurations, initializes data ingestion, generates prompts, and executes the multi-agent system.
    

### config/LoadConfig.py

*   Manages configuration loading and validation.
    

### translation\_data\_ingest/TranslationDataIngest.py

*   Handles data and ontology ingestion, schema validation, and task prompt generation.
    

### mas/MultiAgentSystem.py

*   Executes multi-agent workflows for translation tasks using LLMs.
    

Logging
-------

Logs are stored in the file defined in the configuration (`translation_log.log`). Example log output:  

```
2024-11-27 10:00:00 - __main__  - INFO - DATA TRANSLATION WORKFLOW STARTED
2024-11-27 10:00:05 - TranslationDataIngest - INFO - Successfully loaded source data.
2024-11-27 10:00:10 - MultiAgentSystem - INFO - Multi-agent system task completed successfully.
2024-11-27 10:00:15 - __main__  - INFO - DATA TRANSLATION WORKFLOW ENDED
```  

Contributing
------------

1.  Fork the repository.
    
2.  git checkout -b feature-branch
    
3.  git add -A && git commit -m "Add new feature"
    
4.  Push the branch and open a pull request.
    

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.

Contact
-------

For questions or support, contact **Senol Isci** at [Senol.Isci@digicatapult.org.uk](mailto:Senol.Isci@digicatapult.org.uk).