# AI-Based Test Scenario Generation Using an LLM
# Illustrative example: Playwright with TypeScript

PROMPT = """
You are a senior QA engineer. Given the user story and acceptance criteria,
produce Playwright (TypeScript) tests covering positive, negative, and boundary cases.
Return only code. Do not invent endpoints or selectors not present in the input.

User story: {story}
Acceptance criteria: {criteria}
"""


def build_prompt(story: str, criteria: list[str]) -> str:
    """Build an LLM prompt from a user story and acceptance criteria."""
    return PROMPT.format(
        story=story, criteria="\n".join(f"- {criterion}" for criterion in criteria)
    )


def requires_review(generated_code: str) -> bool:
    """Flag generated code that requires human review."""
    risky = ["eval(", "process.env", "DROP TABLE"]

    return (
        any(token in generated_code for token in risky)
        or "expect(" not in generated_code
    )


# Example user story
story = (
    "As a user, I want to log in with my email and password "
    "so that I can access my account."
)

# Acceptance criteria
criteria = [
    "Valid credentials allow the user to log in.",
    "Invalid credentials display an error message.",
    "Empty email or password fields are rejected.",
]

# Build and display the prompt
prompt = build_prompt(story, criteria)

print("=== GENERATED PROMPT ===")
print(prompt)

# Example generated test code for demonstrating the review function
generated_code = """
import { test, expect } from '@playwright/test';

test('login form displays correctly', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
});
"""

# Screen the generated code
print("\n=== HUMAN REVIEW CHECK ===")

if requires_review(generated_code):
    print("Review required: inspect the generated code before merging.")
else:
    print("No configured warning detected. Further validation is still required.")

print("\n=== GENERATED TEST CODE ===")
print(generated_code)
