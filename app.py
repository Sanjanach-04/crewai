import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM

# --- Page Config ---
st.set_page_config(
    page_title="Multi-Agent AI Demo",
    page_icon="🤖",
    layout="centered"
)

# --- Sidebar ---
st.sidebar.title("🔐 Configuration")
groq_key = st.sidebar.text_input("Enter GROQ API Key", type="password")

# --- Main UI ---
st.title("CREW AI 101 🤖🧠")
st.markdown("Multi-Agent AI System (Researcher + Writer)")

# --- Workflow ---
st.subheader("Agent Workflow")
st.graphviz_chart("""
digraph {
    "User Input" -> "Research Agent" -> "Writer Agent" -> "Final Output"
}
""")

st.markdown("---")

# --- User Input ---
topic = st.text_input(
    "Enter topic:",
    "Latest Generative AI breakthroughs"
)

output_format = st.selectbox(
    "Select output format:",
    ["Blog Post", "Detailed Report", "Simple Summary"]
)

# --- Run Button ---
if st.button("🚀 Start AI Agents"):

    if not groq_key:
        st.error("❌ Please enter GROQ API key")
    else:
        try:
            os.environ["GROQ_API_KEY"] = groq_key

            st.subheader("⚙️ Agent Execution")

            # ✅ Controlled LLM (short output)
            llm = LLM(
                model="groq/llama-3.3-70b-versatile",
                api_key=groq_key,
                max_tokens=500
            )

            # --- Agents ---
            researcher = Agent(
                role="Researcher",
                goal="Find key insights",
                backstory="Expert researcher who summarizes information",
                llm=llm,
                verbose=True
            )

            writer = Agent(
                role="Writer",
                goal="Write short and clear content",
                backstory="Professional writer who keeps content concise",
                llm=llm,
                verbose=True
            )

            # --- Tasks (CONTROLLED OUTPUT) ---
            research_task = Task(
                description=f"""
                Research about {topic}.
                
                Give ONLY:
                - 5 key points
                - Each point in 1–2 lines
                - No extra explanation
                """,
                agent=researcher,
                expected_output="5 concise bullet points only"
            )

            writer_task = Task(
                description=f"""
                Write a {output_format} on {topic}.
                
                Rules:
                - Max 150 words
                - Simple language
                - No repetition
                """,
                agent=writer,
                expected_output="Short summary under 150 words"
            )

            # --- Crew ---
            crew = Crew(
                agents=[researcher, writer],
                tasks=[research_task, writer_task],
                process=Process.sequential,
                verbose=True
            )

            # --- Run ---
            result = crew.kickoff()

            st.success("✅ AI Agents Completed Successfully!")

            # --- Clean Output UI ---
            st.subheader("📄 Results")

            st.markdown("### 🧠 Research Agent Output")
            st.write(result.tasks_output[0].raw)

            st.markdown("### ✍️ Writer Agent Output")
            final_output = result.tasks_output[1].raw
            st.write(final_output)

            # --- Download Button ---
            st.download_button(
                label="📥 Download Output",
                data=final_output,
                file_name="ai_output.txt"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.exception(e)