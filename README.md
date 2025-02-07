# TSCE-LLM
TSCE-LLM: A large language model text summarization capabilities evaluator

This project evaluates Chinese text summarization capabilities across LLM models like Qwen2-VL-72B, DeepSeek-V3, DeepSeek-R1, and gpt-4o using standardized rules. It supports evaluation via online API and local Ollama integration.

Evaluation Criteria
--
Evaluation follows the "Large Language Model News Summarization Evaluation System Standards":

  * Accuracy: Does the summary accurately reflect the key information of the news?
  * Completeness: Does the summary cover the main events, individuals, time, and location?
  * Conciseness: Is the summary concise and non-redundant?
  * Language Fluency: Is the language of the summary smooth and suitable for written expression?
  * Logical Clarity: Is the structure of the summary clear, and are logical relationships evident?

Each criterion is scored on a scale from 0 to 10. The final score is the average of these scores after equal weighting.

Results
--
Based on the experiment results, here are the scores for each model evaluated:

| Models | Scores |
|:------:|:--------:|
| DeepSeek-R1 | 8.78 |
| DeepSeek-V3 | 8.64 |
| Qwen2-VL-72B | 7.66 |
| GPT-4o | 8.66 |
<figcaption style="text-align: center;">* Referee Model: GPT-3.5-turbo.</figcaption>
