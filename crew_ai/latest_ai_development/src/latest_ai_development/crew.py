from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.command_runner_tool import CommandRunnerTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class LatestAiDevelopment():
	"""LatestAiDevelopment crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools

	# Add new agents
	# @agent
	# def product_owner_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['product_owner_agent'],
	# 		verbose=True
	# 	)

	@agent
	def describe_success_criteria_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['describe_success_criteria_agent'],
			verbose=True
		)

	@agent
	def developer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['developer_agent'],
			verbose=True,
			tools=[CommandRunnerTool()]
		)

	# @agent
	# def rag_with_docs_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['rag_with_docs_agent'],
	# 		verbose=True
	# 	)

	@agent
	def tester_unit_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['tester_unit_agent'],
			verbose=True
		)

	# @agent
	# def db_analyst_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['db_analyst_agent'],
	# 		verbose=True
	# 	)

	@agent
	def reviewer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['reviewer_agent'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task

	# Add new tasks
	# @task
	# def product_owner_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['product_owner_task'],
	# 	)

	@task
	def success_criteria_task(self) -> Task:
		return Task(
			config=self.tasks_config['success_criteria_task'],
		)

	@task
	def development_task(self) -> Task:
		return Task(
			config=self.tasks_config['development_task'],
		)

	# @task
	# def documentation_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['documentation_task'],
	# 	)

	@task
	def unit_testing_task(self) -> Task:
		return Task(
			config=self.tasks_config['unit_testing_task'],
		)

	# @task
	# def database_analysis_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['database_analysis_task'],
	# 	)

	@task
	def solution_review_task(self) -> Task:
		return Task(
			config=self.tasks_config['solution_review_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the LatestAiDevelopment crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=[self.describe_success_criteria_agent(),  self.developer_agent(), self.tester_unit_agent(), self.reviewer_agent()], # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
