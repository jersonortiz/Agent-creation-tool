from crewai import Agent, Task, Crew, Process
from langchain.agents import AgentType, initialize_agent, load_tools

human_tools = load_tools(["human"])



# Define Agents
email_writer_1 = Agent(
    role='Concise Email Writer',
    goal='Write a short and engaging email',
    backstory='Experienced in writing concise marketing emails.',
    verbose=True,
    allow_delegation=False
)

dtc_cmo = Agent(
    role='DTC CMO',
    goal='Lead the team in creating effective cold emails',
    backstory='A CMO who frequently receives marketing emails and knows what stands out.',
    verbose=True,
    allow_delegation=True,
    # Passing human tools to the agent
    tools=human_tools
)

copywriter = Agent(
    role='Professional Copywriter',
    goal='Critique and refine the email content',
    backstory='A professional copywriter with extensive experience in persuasive writing.',
    verbose=True,
    allow_delegation=False
)

# Define Task
email_task = Task(
    description="""1. Write three variations of a cold email selling a video editing solution . 
    Ask Human for advice on how to write a cold email.
    2. Critique the written emails for effectiveness and engagement.
    3. Proofread the emails for grammatical correctness and clarity.
    4. Adjust the emails to ensure they meet cold outreach best practices. make sure to take into account the feedback from human 
    which is a tool provided to dtc_cmo.
    5. Rewrite the emails based on all feedback to create three final versions.
    6. take in care the sender of the email is {your name} whith the email {sender email} 
    7 take in care the email receiver is {receiver} whith the email {receiver mail}: """,
    expected_output="""oranize the emails in a text file """,
    output_file='mails.txt',
    agent=dtc_cmo  # DTC CMO is in charge and can delegate
)

# Create a Single Crew
email_crew = Crew(
    agents=[email_writer_1,dtc_cmo, copywriter],
    tasks=[email_task],
    verbose=True,
    process=Process.sequential,
    embedder={
        "provider": "gpt4all"
    }

)

# Execution Flow
print("Crew: Working on Email Task")
final_emails = email_crew.kickoff(inputs={'your name': 'jerson ortiz',
                                          'sender email':'jersonortiz9696@gmail.com',
                                          'receiver':'juan perez',
                                          'receiver mail': 'juan@gmail.com'
                                          })