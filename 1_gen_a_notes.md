## Section 14: Core Foundations of Gen AI (Context)

- How LLMs work:
  - The transformer (black box of the LLMs) basically only predicts the next token. So when we send a message, it basically loops by:
    - predicting the next token;
    - appending it to the original;
    - checking again the original updated token for the next token prediction

- Implementing a Custom Tokenizer
  - OpenAI has an open library: `tiktoken`
  - So we can create encoder to encode / decode depending on the model

- Transformer Model Architecture
  - <img src="./assets/images/transformer_model_arch.png" alt="Transformer Model Architecture" width="420" />

- Vector embeddings are numerical representations of data points, that capture their meaning and relationships
  - [tensorflow projector](https://projector.tensorflow.org/)

- Positional Encoding is basically creating an array of the vector for setting the proper order

- Self Attention
  - How context might affect the meaning of the word - e.g. River Bank vs Finnancial Bank

- At the end, in Linear, its basically defining the probabilities of each possible token to be the next token, to then define the most probable

## Section 15: API Setup

- OpenAI is 100% paid for API usage
- Gemini has a free tier
- Since this course will use Open AI, Gemini has the Gemini OpenAI api - its possible to use the OpenAI api via Gemini API (Gemini surely made it to let projects to migrate from OpenAI to Gemini)

## Section 16: Prompt Engineering

- When we are createing the prompt, there is:
  - System or developer role (also instructions for newer. versions)

- Instructions patterns:
  - Define 'shots'
    - Zero Shot Prompting
      - DIrectly giving the instruction for the model - like "if its not math related, just reply 'sorry'"

    - Few Shot Prompting (more commonly used and more precise)
      - Give some examples in the prompt

  - Define structured Outputs
    - e.g.: Ask a specific JSON output format

  - Add a persona (preferably with examples)

  - Determine Chain of Thought - CoT
    - Add in the instructions I want the model to plan until he decides its enough and send me back an output
    - So, we can use the chain of thought by appending to the prompt the steps the LLM gives us, and looping it
      - [Example:](./assets/udemy-genai-python-main/16_prompts/3_cot.py)
    - But as I understand in current models we dont need to loop responses like this, just add in the promtpt we want proper reasoning
      - Also in my test, it didnt make a difference

## Section 17: Prompt Styles

- Alpaca Prompt:
  - Instructions
  - Input
  - Response

- ChatML
  -as we are doing, with an object defining role and content

- INST Prompting

## Section 18: Local LLM Deployment & API Integration

- Run LLMs offline
  - DeepSeek, Qwen, Llama, Gemma, ar emodels you can download and run offline

- So instead of downloading and installing it locally, we can run these things on a Docker container in our machine
  - Basically the module was about running it locally, and having a basic fastApi also running locally to send messages to LLM, parse back responses

## Section 19: Hugging Face

- Hugging Face is like a hub/registry for AI models, datasets and demos
  - Mental model: GitHub + npm/pip registry for AI

- Practical use: search for models that fit the task, check license/commercial usage and hardware requirements, then use via API or download/run locally if possible

- Obs.: being available on Hugging Face does not mean it is easy to run locally; some models require strong GPU, lots of RAM or accepting usage terms

- For now: understand how to find and consume existing models; no need to deeply learn model training/deployment yet

## Section 20: Agentic AI

- When we "convert" a LLM into a agent we expand its capabilities to perform actions, such as accessing DBs
  - Basically we give if tools (functions, apis etc) so it can run then while thinking
  - Thats why its important to add the chain of thought

- Weather Agent: [agent.py](./src/20_AI_Agent/main.py)
  - We want to create an agent that check the current weather via api (which depends on the city as an arg)
  - User inputs the city;
  - Basically we create the function to fetch the data from the api;
  - We create a chain of thought to the agent, where we list all tools it has access, and it decides what tool he will use depending on the context of the input

- **Structured Output**
  - When I want a structured Output, I should:
  1. Create the pydantic class;
  2. Define the text_format in the req;
  3. Extract it as `parsed_result = response.output_parsed`

  ```python
            response = client.responses.parse(
            model="gpt-5.5",
            instructions=SYSTEM_PROMPT,
            input=message_history,
            text_format=Output,
        )

  ```

- Create a CLI coding agent:
  - Basically we create a tool function to the agent to runa. command on sistem:
  ```python
      def run_command (cmd:str):
        result = os.system(cmd)
        return result
  ```

## Section 21 - PDF Project with RAG

RAG = Retrieval Augmented Generation.

It solves this problem: the LLM does not automatically know the content of my private files, and sending the full PDF in every prompt would be expensive, slow, and limited by the model context window.

So instead of sending the whole document every time, we:

1. Index the document once
2. Retrieve only the most relevant chunks for each user question
3. Send those chunks as context to the LLM
4. Ask the LLM to answer based only on that context

---

### Mental Model

```text
PDF
→ pages
→ text chunks
→ embeddings
→ vector database
→ user question
→ question embedding
→ similar chunks
→ LLM answer with context
```

---

### Main Components

- `PyPDFLoader`
  - Loads the PDF and converts each page into a LangChain document

- `RecursiveCharacterTextSplitter`
  - Splits large pages into smaller text chunks
  - `chunk_size=1000`: each chunk has around 1000 characters
  - `chunk_overlap=400`: part of the previous chunk is repeated in the next chunk to preserve context

- `OpenAIEmbeddings`
  - Converts text into vectors/numbers that represent semantic meaning
  - Similar meanings should produce similar vectors

- `QdrantVectorStore`
  - Stores the chunks and their embeddings
  - Allows similarity search: “find chunks semantically close to this question”

- `OpenAI`
  - Receives the retrieved context + user question
  - Generates the final answer

---

### Indexing Phase (`index.py`)

This phase prepares the PDF for search.

```text
Load PDF
→ split into chunks
→ create embeddings
→ store in Qdrant collection
```

Important line:

```python
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url=VECTOR_STORE_URL,
    collection_name="learning_rag",
)
```

Meaning:

- `documents=chunks`: text chunks that will be stored
- `embedding=embedding_model`: model used to convert each chunk into vectors
- `url=VECTOR_STORE_URL`: where Qdrant is running locally
- `collection_name="learning_rag"`: name of the vector DB collection/table-like storage

This script only needs to run when indexing or re-indexing the PDF.

---

### Retrieval Phase (`chat.py`)

This phase answers user questions using the indexed PDF.

```text
User asks a question
→ convert question into embedding
→ search similar chunks in Qdrant
→ build context from retrieved chunks
→ send context + question to LLM
→ print answer
```

Important line:

```python
search_results = vector_db.similarity_search(query=user_query)
```

Meaning:

- The user question is converted into an embedding
- Qdrant finds the most semantically similar chunks from the PDF
- Those chunks become the context for the LLM

The LLM should not answer from general knowledge. It should answer only from the retrieved PDF context.

---

### Docker / Qdrant

Qdrant is the vector database used in this project.

We run it locally with Docker so we do not need to manually install Qdrant on the machine.

`docker-compose.yml`:

```yaml
services:
  vector-db:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
```

Run:

```bash
docker compose up
```

Qdrant runs at:

```text
http://localhost:6333
```

---

### Dependencies

```bash
pip install -U langchain-community pypdf
pip install -U langchain-text-splitters
pip install -U langchain-openai
pip install -U langchain-qdrant
```

---

### Big Picture

This project is not “the AI reads the PDF directly.”

It is:

```text
The app searches the PDF first, retrieves only the relevant parts, and gives those parts to the LLM so it can answer with document context.
```

That is the core idea of RAG.

## Section 22 - Scalable RAG with Async Queues & Distributed Workers

- We must make it asyncronous, so the system is not blocked while the RAG is being used
  - So we need to create:
    - queue orchestrating logic
    - FastAPI server - so we will have a query and a result routes

- Instead of the API doing the RAG search + LLM call synchronously (blocking the request), it just pushes the job into a queue and immediately returns a `job_id`. A separate worker process picks up jobs from the queue and processes them whenever it can.

---

### Mental Model

```text
client
→ POST /chat (query)
→ enqueue job in Redis/Valkey
→ return job_id immediately
→ worker picks job from queue
→ worker runs the RAG pipeline (from Section 21)
→ result stored on the job
→ client polls GET /job-status (job_id)
→ result
```

---

### Queues in System Design

- We are going to push the request into a queue (FIFO)
- This decouples "receiving the request" from "processing the request" - the API stays fast/responsive, and heavy work (embeddings + LLM call) happens in the background

### Implementing the Queues

- For the Queues, we need to use RQ system, which needs Redis (or Valkey - its the same code, but Redis is not open sourced anymore)

- `pip install rq`

- Basically, we will create the query processing as a util function (`process_query`) and use redis to enqueue it in our server

### Main Components

- `client/rq_client.py`
  - Creates the `queue` object, connected to Redis/Valkey running locally

  ```python
  queue = Queue(connection=Redis(host="localhost", port=6379))
  ```

- `queues/worker.py`
  - Holds `process_query`, the actual RAG logic (same idea as Section 21's `chat.py`): similarity search on Qdrant, build context, call the LLM, return the answer
  - This is the function that gets executed by the worker process, not by the API process

- `server.py`
  - `POST /chat`: enqueues `process_query` with the user's query and immediately returns `{"status": "queued", "job_id": ...}`
    ```python
    job = queue.enqueue(process_query, query)
    ```
  - `GET /job-status`: given a `job_id`, fetches the job from the queue and returns its result (`None` while still processing)
    ```python
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    ```

- `main.py`
  - Entry point, just runs the FastAPI app with `uvicorn`

### Running the Worker

- The API only enqueues jobs - something else has to consume them. That's the RQ worker, run as a separate process:
  ```bash
  rq worker
  ```
- **Obs.:** Had to run `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` in terminal to run on mac (RQ forks a process per job, and macOS's Objective-C runtime crashes on fork when certain frameworks were already initialized)

### Obs.: Imports

- Files inside `22_rag_quere` use plain sibling imports (`from server import app`, `from queues.worker import process_query`), not relative imports (`from .server import app`)
  - `main.py`/`server.py` are run directly as scripts (not via `python -m`), and the folder name (`22_rag_quere`) starts with a digit, so it can't be treated as a real Python package anyway

### Docker / Valkey

`docker-compose.yml`:

```yaml
services:
  valkey:
    image: valkey/valkey
    ports:
      - "6379:6379"
```

Run:

```bash
docker compose up -d
```

## Section 23 - Multi Modal Agents

- LLM that process different data types (text, image, audio etc)

- In GPT api it is basically adding more content items in the array
  - For each model we can simply check what types are supported in the input and output formats

## Section 24 - Agentic Workflows and LangGraph

- Many times we need to create a workflow, like:
  - user_query > planning > Decide the flow branch:
    - Do Web Search
    - Simple LLM Call
  - Get a 2nd LLM to review the response
    - Review and update
    - End flow

- So LangGraph exists for these agentic workflows
  - In LangGraph you have the Nodes (functions)
  - We connect the Nodes with Edges
  - Than we have a state (a piece of data), which will pass by each node

- LangGraph is used to build stateful AI workflows.
- Nodes are functions/steps.
- Edges define what runs after what (chains the nodes).
- State is the shared data passed through the graph.
- Each node receives the current state and returns updates to the state.
- Useful when workflows have branching, loops, tool calls, reviews, retries, or multiple steps.
- For simple linear code, normal function chaining may be enough.

### Setup:

- `pip install -U langgraph`

- Create the graph_builder:

  ```python
    class State(TypedDict):
      messages: Annotated[list, add_messages]

    graph_builder = StateGraph(State)
  ```

  - Create the nodes, chain them with the Edges and then compile (also setting the initial state):

    ```python
        def sample_node(state: State):
          pass

        def random_node(state: State):
          pass


        graph_builder = StateGraph(State)

        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_node("sample_node", sample_node)

        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", "sample_node")
        graph_builder.add_edge("sample_node", END)

        graph = graph_builder.compile()

        initial_state = State({"messages": ["What is my name?"]})
        final_state = graph.invoke(initial_state)
    ```
