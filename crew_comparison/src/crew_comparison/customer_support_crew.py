from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.email_ingestion_tool import EmailIngestionTool
from tools.sentiment_analysis_tool import SentimentAnalysisTool
from tools.faq_lookup_tool import FAQLookupTool
from tools.escalation_decision_tool import EscalationDecisionTool
from langchain_openai import ChatOpenAI


@CrewBase
class CustomerSupportCrew():
    """CustomerSupportCrew crew"""

    agents_config = 'config/customer_support_agents.yaml'
    tasks_config = 'config/customer_support_tasks.yaml'

    # Agent definitions
    @agent
    def email_ingestion_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['email_ingestion_agent'],
            verbose=True,
            tools=[EmailIngestionTool()]
        )

    @agent
    def sentiment_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sentiment_analysis_agent'],
            verbose=True,
            tools=[SentimentAnalysisTool()]
        )

    @agent
    def faq_knowledge_base_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['faq_knowledge_base_agent'],
            verbose=True,
            tools=[FAQLookupTool()]
        )

    @agent
    def escalation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['escalation_agent'],
            verbose=True,
            tools=[EscalationDecisionTool()]
        )

    # Task definitions
    @task
    def email_ingestion_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_ingestion_task'],
        )

    @task
    def sentiment_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['sentiment_analysis_task'],
        )

    @task
    def faq_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['faq_search_task'],
        )

    @task
    def escalation_decision_task(self) -> Task:
        return Task(
            config=self.tasks_config['escalation_decision_task'],
        )

    # Crew definition
    @crew
    def crew(self) -> Crew:
        """Creates the CustomerSupportCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator,
            manager_llm=ChatOpenAI(temperature=0, model="gpt-4o-mini"),
            process=Process.hierarchical,
            planning=False,
            verbose=True,
        )
