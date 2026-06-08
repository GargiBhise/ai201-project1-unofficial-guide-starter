import gradio as gr

from generate import ask


def handle_query(question):
    """
    Gradio wrapper for the RAG system.

    Takes a user question and returns:
    - grounded answer
    - source filenames
    """
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    answer = result["answer"]
    sources = "\n".join(f"- {source}" for source in result["sources"])

    return answer, sources


with gr.Blocks() as demo:
    gr.Markdown("# Unofficial Guide: Cal Poly Pomona CS Professor Reviews")
    gr.Markdown(
        "Ask questions about student reviews of Computer Science professors at Cal Poly Pomona."
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="Example: Which professor is described as test-heavy?",
        lines=2,
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Retrieved from", lines=5)

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[answer, sources],
    )

    question.submit(
        handle_query,
        inputs=question,
        outputs=[answer, sources],
    )


if __name__ == "__main__":
    demo.launch()