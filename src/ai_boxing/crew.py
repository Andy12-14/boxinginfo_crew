from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai import LLM
from ai_boxing.tools.custom_tool import WhatsAppTool, SearchTool


llm = LLM(
    # Use a smaller, faster model for local testing to avoid long startup/response times.
    # Switch to 'ollama/gemma3:latest' (smaller ~3GB model) while debugging timeouts.
    model="ollama/gemma3:latest",
    config={
        # shorter timeouts while developing so failures surface quickly
        "timeout": 30,  # 30 seconds overall
        "request_timeout": 30,  # 30 seconds per HTTP request
        "context_window": 2048,
        "temperature": 0.7,
        # stream helps get partial output sooner
        "stream": True,
        # keep responses short while testing
        "max_output_tokens": 256,
    }
)


@CrewBase
class AiBoxing():
    """AiBoxing crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    
    @agent
    def boxer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['boxer_agent'], # type: ignore[index]
            verbose=True,
            llm=llm,
            tools=[SearchTool()]
        )

    @agent
    def reporter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter_agent'], # type: ignore[index]
            verbose=True,
            llm=llm,
            tools=[SearchTool(), WhatsAppTool()]
        )

    @task
    def boxer_task(self) -> Task:
        return Task(
            config=self.tasks_config['boxer_task'], # type: ignore[index]
        )

    @task
    def reporter_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporter_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiBoxing crew"""
        

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
