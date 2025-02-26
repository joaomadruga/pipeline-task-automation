from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.paper_crawler_tool import PaperCrawlerTool
from tools.text_extraction_tool import TextExtractionTool
from tools.summarization_tool import SummarizationTool
from tools.topic_classifier_tool import TopicClassifierTool
from tools.report_generator_tool import ReportGeneratorTool
from langchain_openai import ChatOpenAI


@CrewBase
class ResearchCrew():
    """ResearchCrew crew"""

    agents_config = 'config/research_agents.yaml'
    tasks_config = 'config/research_tasks.yaml'

    # Agent definitions
    @agent
    def paper_crawler_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['paper_crawler_agent'],
            verbose=True,
            tools=[PaperCrawlerTool()]
        )

    @agent
    def text_extraction_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['text_extraction_agent'],
            verbose=True,
            tools=[TextExtractionTool()]
        )

    @agent
    def summarization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summarization_agent'],
            verbose=True,
            tools=[SummarizationTool()]
        )

    @agent
    def topic_classifier_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['topic_classifier_agent'],
            verbose=True,
            tools=[TopicClassifierTool()]
        )

    @agent
    def report_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator_agent'],
            verbose=True,
            tools=[ReportGeneratorTool()]
        )

    # Task definitions
    @task
    def paper_crawling_task(self) -> Task:
        return Task(
            config=self.tasks_config['paper_crawling_task'],
        )

    @task
    def text_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['text_extraction_task'],
        )

    @task
    def summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarization_task'],
        )

    @task
    def topic_classification_task(self) -> Task:
        return Task(
            config=self.tasks_config['topic_classification_task'],
        )

    @task
    def report_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_generation_task'],
        )

    # Crew definition
    @crew
    def crew(self) -> Crew:
        """Creates the ResearchCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            manager_llm=ChatOpenAI(temperature=0, model="gpt-4o-mini"),
            process=Process.hierarchical,
            planning=False,
            verbose=True,
        )
