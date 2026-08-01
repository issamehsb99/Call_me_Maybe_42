*This project has been created as part of the 42 curriculum by ihasbi.*

# Call_me_Maybe_42

Call Me Maybe converts natural language prompts into valid JSON function calls using a small LLM and constrained decoding. It selects the correct function, extracts typed arguments, and guarantees structured, machine-readable output for AI agents and API-based systems.

## Description

This project introduces students to the fundamentals of artificial intelligence, machine learning, deep learning, natural language processing (NLP), and large language models (LLMs).

The main objective is to understand **constrained decoding** rather than relying only on prompt engineering. The model is forced to generate outputs that follow a predefined JSON schema, making the results reliable and easy to integrate into software systems.

### Goal

The program reads prompts from a JSON file, selects the appropriate function, extracts the required parameters, and writes the final function calls to an output JSON file in a valid format.

## Algorithm explanation

### Constrained decoding

Constrained decoding is a decoding strategy that restricts the model so that it can only generate valid tokens according to a predefined schema.

In this project, constrained decoding ensures not only **syntactically valid JSON**, but also **schema-valid JSON**.

The algorithm works by modifying the model logits at each decoding step:

* Valid tokens keep their original logits.
* Invalid tokens are assigned a value of `-inf`.
* The next token is selected using `argmax`, which forces the model to choose only among the allowed tokens.

This guarantees that the generated output always follows the expected JSON structure.

## Design decisions

Several design choices were made to simplify the implementation and improve reliability:

* **NumPy** is used for efficient operations on logits, especially functions such as `full_like` and `argmax`.
* **Pydantic** is used to validate the generated function calls and ensure that the output matches the expected schema.
* The implementation focuses on deterministic decoding rather than probabilistic sampling to maximize correctness.

## Instructions

### Installation

Install the required dependencies:

```bash
make install
```

### Execution

Run the program:

```bash
make run
```

## Example usage

### Input prompt

```json
[
  {
    "prompt": "greet shreak"
  }
]
```

### Function definition

```json
{
  "name": "fn_greet",
  "description": "Generate a greeting message for a person by name.",
  "parameters": {
    "name": {
      "type": "string"
    }
  }
}
```

### Output

```json
[
  {
    "prompt": "greet shreak",
    "name": "fn_greet",
    "parameters": {
      "name": "shreak"
    }
  }
]
```

## Performance analysis

Using the dataset provided in the subject, the implementation produces results in less than **5 minutes**, which satisfies the project requirements.

The solution achieves approximately **90.9% accuracy** while remaining stable and robust. The constrained decoding approach prevents malformed JSON generation and avoids crashes caused by invalid token sequences.

## Challenges faced

One of the main challenges was obtaining consistent outputs from the small LLM. Prompt quality had a significant impact on the generated results.

Another challenge involved handling special characters and tokenization issues. These problems were solved by carefully inspecting the token IDs and logits during debugging.

Peer learning and collaborative debugging were extremely helpful throughout the project.

## Testing strategy

The implementation was validated by inspecting both:

* the token IDs produced by `model.encode()`, and
* the logits generated during constrained decoding.

This made debugging easier and helped verify that only valid tokens were available at each decoding step. Multiple prompts and function definitions were tested to ensure schema correctness and output reliability.

## Resources

### References


* GeeksforGeeks articles on NLP and machine learning
* Various educational resources on constrained decoding and language models

### AI usage

AI tools were used primarily for:

* explaining theoretical concepts related to LLMs and constrained decoding,
* reviewing implementation ideas,
* improving code documentation,
* and correcting English grammar in the README.

All core implementation, debugging, constrained decoding logic, and project design were developed and understood during the project work.