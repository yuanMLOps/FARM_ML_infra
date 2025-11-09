import pytest
from .chains import answer_grader, generate_answer

@pytest.mark.asyncio
async def test_qa_grader_yes() -> None:
    question = "generative agents"
    answer = """Generative agents are AI systems that combine generative models (like GPT) with autonomous decision-making to simulate realistic, goal-driven behavior over time. They can perceive, plan, act, and reflect — often used to model human-like 
    characters or assistants in simulations, games, or productivity tools."""

    grade = await answer_grader(question, answer)
    assert grade == True

@pytest.mark.asyncio
async def test_generate_answer_yes() -> None:
    question = "what is generative agents"
    context = """Generative agents are AI systems that combine generative models (like GPT) with 
    autonomous decision-making to simulate realistic, goal-driven behavior over time. 
    They can perceive, plan, act, and reflect — often used to model human-like 
    characters or assistants in simulations, games, or productivity tools."""

    generated_answer = await generate_answer(context, question)
    assert len(generated_answer) > 1