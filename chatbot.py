from groq import Groq
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
console = Console()

history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

#screen header
console.print(Panel.fit(
    "[bold green]🤖 My AI Chatbot[/bold green]\n[dim]Powered by Groq AI[/dim]",
    border_style="green"
))
console.print("[dim]Type 'quit' to exit | 'clear' to clear history[/dim]\n")

def save_message(role, message):
    filename = "chat_history.txt"
    with open(filename, "a", encoding="utf-8") as f:
        time = datetime.now().strftime("%H:%M:%S")
        f.write(f"[{time}] {role.upper()}: {message}\n\n")

while True:
    # Get user input
    user_input = console.input("[bold cyan]You: [/bold cyan]").strip()

    if user_input.lower() in ["quit", "exit", "bye"]:
        console.print(Panel("[bold green]Goodbye! 👋[/bold green]", border_style="green"))
        break

    if user_input.lower() == "clear":
        history.clear()
        history.append({"role": "system", "content": "You are a helpful assistant."})
        console.clear()
        console.print("[bold green] Chat history cleared![/bold green]\n")
        continue

    if not user_input:
        continue

    history.append({"role": "user", "content": user_input})
    save_message("you", user_input)

    # Show thinking animation
    with console.status("[bold yellow]Bot is thinking...[/bold yellow]"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=history
            )
            reply = response.choices[0].message.content
            history.append({"role": "assistant", "content": reply})
            save_message("bot", reply)

        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]\n")
            continue

    # Display bot reply in a nice panel
    console.print(Panel(
        Text(reply, style="white"),
        title="[bold green]🤖 Bot[/bold green]",
        border_style="green"
    ))
    console.print()