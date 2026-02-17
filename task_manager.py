import os
from google import genai
from dotenv import load_dotenv

# 1. SETUP
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def extract_tasks(transcript_text):
    """The Brain: Converts raw text into a structured table."""
    prompt = f"""
    You are an expert Project Manager. I will provide a transcript:
    {transcript_text}
    
    TASK:
    Extract all action items into a structured Markdown Table with columns:
    | Task | Person Responsible | Priority (High/Medium/Low) |
    """
    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text
    except:
        return "Task extraction failed."

def generate_executive_brief(task_list):
    """The Summarizer: Creates a 3-sentence brief for leadership."""
    prompt = f"""
    Based on these tasks: {task_list}
    
    Provide a 3-sentence Executive Brief:
    1. The primary objective discussed.
    2. The most urgent high-priority item.
    3. Who owns the next immediate step.
    
    Tone: Professional, direct, and concise.
    """
    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text
    except:
        return "Briefing generation failed."

if __name__ == "__main__":
    file_path = "transcript.txt"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = file.read()
        
        # --- EXECUTION PIPELINE ---
        # 1. Extract the full table
        detailed_tasks = extract_tasks(data)
        
        # 2. Generate the 3-sentence brief
        exec_brief = generate_executive_brief(detailed_tasks)
        
        # 3. SAVE TO FILE (Added encoding="utf-8" to fix the crash)
        with open("Meeting_Action_Items.md", "w", encoding="utf-8") as md_file:
            md_file.write("# 📋 Meeting Action Items Report\n\n")
            md_file.write("## 🚀 Executive Brief\n")
            md_file.write(exec_brief + "\n\n")
            md_file.write("## 📊 Detailed Task Manifest\n")
            md_file.write(detailed_tasks)

        print("\n" + "="*40)
        print("✅ PROJECT B COMPLETE")
        print("Check 'Meeting_Action_Items.md' for the brief and table.")
        print("="*40)
    else:
        print(f"❌ ERROR: I couldn't find '{file_path}'.")