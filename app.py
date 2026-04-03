import os

import gradio as gr
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

ROLES = [
    "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Flutter / Mobile Developer",
    "Mobile Engineer (iOS/Android)",
    "ML / AI Engineer",
    "AI Product Engineer",
    "Data Analyst",
    "Data Scientist",
    "DevOps / Cloud Engineer",
    "Product Manager",
    "UI/UX Designer",
]
COMPANY_TYPES = [
    "FAANG / Big Tech (Google, Meta, Amazon…)",
    "Startup (fast-paced, generalist)",
    "Mid-size Tech Company",
    "Bank / FinTech",
    "Consulting / Agency",
]
EXPERIENCE_LEVELS = [
    "Junior  (0 – 2 years)",
    "Mid-level  (2 – 5 years)",
    "Senior  (5 + years)",
]
MODEL = "llama-3.3-70b-versatile"


def build_system_prompt(role, company_type, experience):
    company_profiles = {
        "FAANG": {
            "focus": "Focus heavily on system design at scale, algorithmic efficiency, distributed systems, performance optimization, and measurable impact. Probe edge cases, failure modes, and trade-offs.",
            "culture": "Data-driven, high bar for technical excellence, collaborative but rigorous.",
            "red_flags": "Vague answers, inability to estimate scale, no ownership of past decisions.",
        },
        "Startup": {
            "focus": "Focus on ownership mentality, speed of execution, product thinking, and ability to work across multiple responsibilities with limited resources.",
            "culture": "High ownership, low process, everyone wears many hats.",
            "red_flags": "Needs heavy structure, no examples of initiative, uncomfortable with ambiguity.",
        },
        "Bank": {
            "focus": "Focus on reliability, security, compliance awareness, process discipline, documentation, and cross-team collaboration.",
            "culture": "Risk-averse, process-heavy, values stability and proven patterns.",
            "red_flags": "Cutting corners, ignoring compliance, poor documentation habits.",
        },
        "Consulting": {
            "focus": "Focus on structured communication, client delivery, stakeholder management, and translating technical concepts for non-technical audiences.",
            "culture": "Client-first, deadline-driven, communication and presentation are paramount.",
            "red_flags": "Poor storytelling, cannot simplify complexity, no client-facing impact examples.",
        },
    }
    level_profiles = {
        "Junior": {
            "note": "Ask foundational questions about core concepts, problem-solving approach, and learning mindset. Reward intellectual honesty. Focus on curiosity and coachability.",
            "signal": "Growth mindset, foundational knowledge, learning velocity, coachability.",
            "depth": "foundational",
        },
        "Mid": {
            "note": "Test independent thinking, practical experience, debugging ability, and architecture awareness. Push back on shallow answers.",
            "signal": "Ownership, technical range, cross-functional communication, real-world trade-offs.",
            "depth": "applied",
        },
        "Senior": {
            "note": "Hold a high bar. Expect system design fluency, mentorship examples, and strategic influence. Push hard on ambiguous scenarios.",
            "signal": "Leadership without authority, technical vision, force-multiplier behaviors.",
            "depth": "strategic",
        },
    }
    company_key = next((k for k in company_profiles if k in company_type), None)
    level_key = next((k for k in level_profiles if k in experience), "Mid")
    company = company_profiles.get(
        company_key,
        {
            "focus": "Balance technical depth with communication, product thinking, and business impact.",
            "culture": "Values well-rounded engineers who ship quality software.",
            "red_flags": "Overcomplicating problems, poor communication, no concrete impact examples.",
        },
    )
    level = level_profiles[level_key]

    return f"""You are a highly experienced technical interviewer conducting a realistic hiring interview.
You are human, warm, and professional — not a robot. React naturally to what the candidate says.

INTERVIEW CONTEXT
Role: {role} | Level: {experience} ({level["depth"]} depth) | Company: {company_type}

COMPANY PROFILE
Focus:   {company["focus"]}
Culture: {company["culture"]}
Red Flags (watch silently, never mention): {company["red_flags"]}

EXPERIENCE EXPECTATIONS
{level["note"]}
Key Signal: {level["signal"]}

INTERVIEW FLOW
1. Open with a brief natural greeting and ask the candidate to introduce themselves.
2. Ask ONE question at a time. Never stack multiple questions.
3. After each answer, use your human judgment to decide what feedback to give:

   FEEDBACK RULES — read carefully:
   - Feedback must ONLY be about what the question was actually asking. Never bring up unrelated topics.
   - For simple intro questions (name, years of experience, background): skip feedback entirely. Just respond naturally like a human interviewer would and move to the next question.
   - For real interview questions, internally score the answer from 1–10, then choose ONE of these:

     a) Answer is strong (score 8.5+):
        ✅ Strong: [max 2 lines — what specifically was good, relevant to the question asked]
        Then move to the next question.

     b) Answer is weak (score below 5):
        ⚠️ Weak: [max 2 lines — what was specifically missing, relevant to the question asked]
        Then move to the next question.

     c) Answer has both good and bad parts (score 5–8.4):
        ✅ Strong: [max 2 lines — the good part]
        ⚠️ Weak: [max 2 lines — what was missing]
        Then move to the next question.

   - NEVER force feedback when the answer is an intro or small talk.
   - NEVER mention things outside the scope of the question asked.
   - Keep feedback short, honest, and directly tied to the question.

4. Gradually increase difficulty as the interview progresses.

5. ADAPTIVE INTERVIEW LENGTH — follow this logic strictly:

   You are tracking two things internally: question count and a "strike" counter.
   A strike is added when a score is below 5 (bad answer). A strike is removed when a score is 8.5+ (great answer).

   EARLY TERMINATION (after minimum 5 questions):
   - If the candidate accumulates 3 strikes with scores below 5 → end the interview early. Say: "That wraps up our interview today." This signals they are not ready.
   - If the candidate scores 8.5+ on 3 consecutive answers after question 5 → end the interview early. Say: "That wraps up our interview today." This signals they are clearly strong.

   EXTENDED INTERVIEW (questions 5–15):
   - If the candidate's average score is above 7 after question 5 → target 10–12 questions total to give them a fair chance to shine.
   - If answers are inconsistent (mixed strong and weak) → continue up to 15 questions max.
   - Never exceed 15 questions under any circumstances.

   NORMAL END:
   - If none of the above triggers, wrap up naturally between questions 5–15.

6. When ending the interview for any reason, always say exactly: "That wraps up our interview today."
   Then add on a new line: "💡 Type 'my score', 'my evaluation', or 'hiring decision' to see your full report."
   Wait for the candidate to ask before showing the report.

7. User can ending intreview anytime by typing 'end interview' or 'end' or 'finish'

WHEN CANDIDATE ASKS FOR SCORE / EVALUATION / REPORT:
Produce this report immediately:

══════════════════════════════════
INTERVIEW EVALUATION REPORT
══════════════════════════════════
Role         : {role}
Company Type : {company_type}
Level        : {experience}

OVERALL SCORE : X / 10

STRENGTHS
- ...

AREAS TO IMPROVE
- ...

TIPS FOR NEXT TIME
- ...

HIRING DECISION : [Strong Yes / Yes / Maybe / No]
══════════════════════════════════

RULES
- Stay fully in character. NEVER say you are an AI.
- NEVER output raw Python dicts, lists, or JSON. Always respond in plain text only.
- Do NOT reveal scores or red flags during the interview.
- If answers are vague, push back naturally: "Can you walk me through that a bit more?"
- React like a human — if something is impressive, show it. If something is off, be direct but respectful."""


def call_groq(messages):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=900,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Groq API error: {e}")


def extract_text(content):
    """Safely extract plain text from any content format Gradio might pass."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
        return " ".join(parts).strip()
    if isinstance(content, dict):
        return content.get("text", str(content))
    return str(content)


def history_to_groq(system_prompt, history):
    """Convert Gradio 6 messages history to Groq API messages format."""
    msgs = [{"role": "system", "content": system_prompt}]
    for msg in history:
        role = msg.get("role", "")
        content = extract_text(msg.get("content", ""))
        if role == "user":
            clean = content.replace("🎤 ", "").strip()
            if clean:
                msgs.append({"role": "user", "content": clean})
        elif role == "assistant":
            if content:
                msgs.append({"role": "assistant", "content": content})
    return msgs


def transcribe_audio(audio_path):
    if not audio_path:
        return ""
    try:
        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=f,
                response_format="text",
            )
        if isinstance(result, str):
            return result.strip()
        return str(result).strip()
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {e}")


def start_interview(role, company_type, experience):
    system_prompt = build_system_prompt(role, company_type, experience)
    msgs = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Please start the interview now."},
    ]
    try:
        opener = call_groq(msgs)
    except RuntimeError as e:
        history = [
            {"role": "assistant", "content": f"⚠️ Failed to start interview: {e}"}
        ]
        return (
            history,
            "",
            gr.update(
                interactive=False, placeholder="Click 'Start Interview' to retry…"
            ),
            gr.update(interactive=False),
            gr.update(interactive=True),
            gr.update(
                value="❌ Could not reach the AI service. Check your API key and internet connection."
            ),
            gr.update(interactive=False),
            gr.update(interactive=False),
        )
    history = [{"role": "assistant", "content": opener}]
    return (
        history,
        system_prompt,
        gr.update(interactive=True, placeholder="Type your answer…"),
        gr.update(interactive=True),
        gr.update(interactive=False),
        gr.update(
            value=f"**Role:** {role}  |  **Company:** {company_type}  |  **Level:** {experience}"
        ),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


def user_reply(user_message, history, system_prompt):
    if not user_message or not user_message.strip():
        return history, ""
    msgs = history_to_groq(system_prompt, history)
    msgs.append({"role": "user", "content": user_message.strip()})
    try:
        ai_response = call_groq(msgs)
    except RuntimeError as e:
        ai_response = f"⚠️ Sorry, something went wrong: {e}\n\nPlease try sending your message again."
    history = history + [
        {"role": "user", "content": user_message.strip()},
        {"role": "assistant", "content": ai_response},
    ]
    return history, ""


def voice_reply(audio_path, history, system_prompt):
    if not audio_path:
        return history, None
    try:
        transcribed = transcribe_audio(audio_path)
    except RuntimeError as e:
        history = history + [
            {"role": "user", "content": "🎤 (voice message)"},
            {
                "role": "assistant",
                "content": f"⚠️ Could not transcribe your audio: {e}\n\nPlease try recording again or type your answer instead.",
            },
        ]
        return history, None
    if not transcribed:
        history = history + [
            {"role": "user", "content": "🎤 (voice message)"},
            {
                "role": "assistant",
                "content": "⚠️ Could not understand the audio. Please try recording again or type your answer instead.",
            },
        ]
        return history, None
    msgs = history_to_groq(system_prompt, history)
    msgs.append({"role": "user", "content": transcribed})
    try:
        ai_response = call_groq(msgs)
    except RuntimeError as e:
        ai_response = f"⚠️ Sorry, something went wrong: {e}\n\nPlease try sending your message again."
    history = history + [
        {"role": "user", "content": f"🎤 {transcribed}"},
        {"role": "assistant", "content": ai_response},
    ]
    return history, None


def reset_all():
    return (
        [],
        "",
        gr.update(interactive=False, placeholder="Click 'Start Interview' first…"),
        gr.update(interactive=False),
        gr.update(interactive=True),
        gr.update(
            value="Configure your interview on the left, then hit **Start Interview**."
        ),
        gr.update(interactive=False),
        gr.update(interactive=False),
    )


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --bg:#0d0f14; --surface:#13161d; --surface2:#1a1e27;
    --accent:#6ee7b7; --accent2:#38bdf8; --text:#e2e8f0;
    --muted:#64748b; --border:#1e2330; --radius:14px;
}
body, .gradio-container { background:var(--bg) !important; font-family:'DM Sans',sans-serif !important; color:var(--text) !important; }
h1,h2,h3 { font-family:'Syne',sans-serif !important; }
#header { background:linear-gradient(135deg,#0f172a,#1e293b); border:1px solid var(--border); border-radius:var(--radius); padding:28px 32px; margin-bottom:20px; }
.panel { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:var(--radius) !important; padding:20px !important; }
.btn-start { background:linear-gradient(135deg,var(--accent),var(--accent2)) !important; color:#0d0f14 !important; font-family:'Syne',sans-serif !important; font-weight:700 !important; border:none !important; border-radius:10px !important; }
.btn-reset { background:var(--surface2) !important; color:var(--muted) !important; border:1px solid var(--border) !important; border-radius:10px !important; }
.chatbot { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:var(--radius) !important; }
#status { background:var(--surface2); border:1px solid var(--border); border-radius:8px; padding:10px 16px; font-size:13px; color:var(--muted); margin-bottom:8px; }
.voice-hint { font-size:12px; color:var(--muted); text-align:center; margin:6px 0; }
.voice-warning { font-size:12px; color:#fbbf24; background:#1a1500; border:1px solid #92400e; border-radius:8px; padding:8px 12px; margin:4px 0; }
label span { font-family:'Syne',sans-serif !important; font-size:13px !important; font-weight:600 !important; color:var(--muted) !important; text-transform:uppercase !important; letter-spacing:0.06em !important; }
"""

with gr.Blocks(title="Intervexa") as demo:
    system_prompt_state = gr.State("")

    with gr.Group(elem_id="header"):
        gr.Markdown("""
# 🎓 Intervexa
### Practice real interviews. Get brutal, honest feedback.
*Powered by AIs: Groq · LLaMA 3.3 70B · Whisper Voice*
*Powered by Maen Khdour.*
        """)

    with gr.Row(equal_height=False):
        with gr.Column(scale=1, min_width=260, elem_classes="panel"):
            gr.Markdown("### ⚙️ Interview Setup")
            role_dd = gr.Dropdown(
                choices=ROLES, value="Software Engineer", label="Job Role"
            )
            company_dd = gr.Dropdown(
                choices=COMPANY_TYPES,
                value="FAANG / Big Tech (Google, Meta, Amazon…)",
                label="Company Type",
            )
            exp_dd = gr.Dropdown(
                choices=EXPERIENCE_LEVELS,
                value="Mid-level  (2 – 5 years)",
                label="Experience Level",
            )
            gr.Markdown("---")
            start_btn = gr.Button(
                "🚀 Start Interview", elem_classes="btn-start", variant="primary"
            )
            reset_btn = gr.Button("🔄 New Interview", elem_classes="btn-reset")
            gr.Markdown("""
---
**How it works**
1. Pick your role & company
2. Hit **Start Interview**
3. Type **or speak** your answers
4. Get your score + report
            """)

        with gr.Column(scale=3):
            status_bar = gr.Markdown(
                "Configure your interview on the left, then hit **Start Interview**.",
                elem_id="status",
            )
            chatbot = gr.Chatbot(height=400, show_label=False, elem_classes="chatbot")

            with gr.Row():
                msg_box = gr.Textbox(
                    placeholder="Click 'Start Interview' first…",
                    label="",
                    scale=5,
                    interactive=False,
                    container=False,
                )
                send_btn = gr.Button(
                    "Send ↵", scale=1, interactive=False, variant="primary"
                )

            gr.Markdown("— or answer with your voice —", elem_classes="voice-hint")
            gr.Markdown(
                "⚠️ After recording, you will see the app is stuck — that is normal, it is processing. Wait ~10 seconds. Do NOT click twice!",
                elem_classes="voice-warning",
            )

            with gr.Row():
                audio_input = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="🎤 Record your answer",
                    interactive=False,
                    scale=4,
                )
                voice_send_btn = gr.Button(
                    "Send 🎤", scale=1, interactive=False, variant="secondary"
                )

    all_outputs = [
        chatbot,
        system_prompt_state,
        msg_box,
        send_btn,
        start_btn,
        status_bar,
        audio_input,
        voice_send_btn,
    ]

    start_btn.click(
        start_interview, inputs=[role_dd, company_dd, exp_dd], outputs=all_outputs
    )
    send_btn.click(
        user_reply,
        inputs=[msg_box, chatbot, system_prompt_state],
        outputs=[chatbot, msg_box],
    )
    msg_box.submit(
        user_reply,
        inputs=[msg_box, chatbot, system_prompt_state],
        outputs=[chatbot, msg_box],
    )
    voice_send_btn.click(
        voice_reply,
        inputs=[audio_input, chatbot, system_prompt_state],
        outputs=[chatbot, audio_input],
    )
    reset_btn.click(reset_all, outputs=all_outputs)

if __name__ == "__main__":
    demo.launch(share=True, css=CSS)
