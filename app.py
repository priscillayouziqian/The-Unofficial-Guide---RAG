import gradio as gr
from generate import ask

def handle_query(question):
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="CUNY Study Abroad QA") as demo:
    gr.Markdown("# 🎓 CUNY Study Abroad Unofficial Guide")
    gr.Markdown("Ask any question about CUNY study abroad programs, financial aid, or credit transfers based on real student reviews.")
    
    with gr.Row():
        inp = gr.Textbox(label="Your question", placeholder="e.g. Can I use my Pell Grant for studying abroad?", scale=4)
        btn = gr.Button("Ask", scale=1, variant="primary")
        
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()