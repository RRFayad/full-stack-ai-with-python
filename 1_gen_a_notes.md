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

- Intructions patterns:
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
