from langchain.prompts import PromptTemplate

def test_steps_to_java_code_prompt_template() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["test_steps", "context"],
        template="""
You are a skilled Java automation engineer working within a custom test automation framework.
Below is the framework code context extracted semantically from relevant files:

Context:
{context}

Below are the Test Case Steps:

{test_steps}

Write Java test code that:
- Uses the utility methods from the framework context above.
- Follows Java best practices.
- Does not include any unnecessary imports or raw Selenium interactions.
- Avoids redundant code or comments.
- Create custom methods and create POM classes if needed and use from their for calling methods.
- Custom POM methods should be created only if necessary, otherwise use the existing methods from the framework.
- Custom POM methods should be for single action, not multiple actions.
- If a method is already available in the framework, reuse it instead of creating a new one.
- If a method is not available in the framework, create a new method for it.
- Use meaningful variable names and method names.
- Use appropriate exception handling.
- Use Java 17 features and syntax.
- Use the provided test steps to guide the implementation.

Respond ONLY with the Java code (as a method or class).
"""
    )
    
def build_test_case_to_java_code_prompt(test_steps: str, context_chunks: list[str]) -> str:
    context = "\n---\n".join(context_chunks)
    prompt_template = test_steps_to_java_code_prompt_template()
    return prompt_template.format(context=context, test_steps=test_steps)
