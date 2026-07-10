import os
from typing import TypedDict, Annotated, List, Literal
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage 
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()


class AgentTask(BaseModel):

    """this class defines the task of the agent. It contains the following attributes:"""

    objective:str = Field(description = "This will contain the objective of this particular agent. It will be a string that describes the task that the agent needs to perform.")
    instructions:str = Field(description = "This will contain the instructions for this particular agent. It will be a string that describes how the agent should perform the task.")

class VentureManager(BaseModel):

    """This class defines the structure of Venture manager agent . It will break down the idea of the user into smaller
    tasks and assign them to the relevant agents. 
    
    The tasks will be divided into the following agents:
    1. Market Research Agent : This agent will be responsible for conducting market research and providing insights on the market size, growth potential, and competitive landscape.
    2. Competitor Analysis Agent : This agent will be responsible for analyzing the competitors in the market and providing insights on their strengths, weaknesses, and strategies.
    3. Customer research Agent : This agent will be responsible for conducting customer research mainly through the llm itself instead of web search and providing insights on customer needs, preferences, and behavior.
    """

    market_research: AgentTask
    competitor_analysis: AgentTask
    customer_research: AgentTask

    """The structure of the output of the agents is predefined and of the form {AgentTask}."""


class MarketResearch(BaseModel):

    """This class defines the structure of Market Research agent. It will conduct market research and provide insights on the market size, growth potential, and competitive landscape."""

    market_size: str = Field(description = "This will contain the market size of the idea. It will be a string that describes the market size in terms of revenue, number of customers, or any other relevant metric.")
    growth_potential: str = Field(description = "This will contain the growth potential of the idea. It will be a string that describes the growth potential in terms of market trends, customer demand, or any other relevant metric.")
    competitive_landscape: str = Field(description = "This will contain the competitive landscape of the idea. It will be a string that describes the competitive landscape in terms of competitors, their strengths and weaknesses, and any other relevant metric.")
    key_insights: str = Field(description = "This will contain the key insights of the market research. It will be a string that summarizes the market research in terms of key findings, insights, and recommendations.")

class CompetitorAnalysis(BaseModel):

    """This class defines the structure of Competitor Analysis agent. It will analyze the competitors in the market and provide insights on their strengths, weaknesses, and strategies."""

    competitor_strengths: str = Field(description = "This will contain the strengths of the competitors. It will be a string that describes the strengths in terms of product features, pricing, marketing strategies, or any other relevant metric.")
    competitor_weaknesses: str = Field(description = "This will contain the weaknesses of the competitors. It will be a string that describes the weaknesses in terms of product features, pricing, marketing strategies, or any other relevant metric.")
    competitor_strategies: str = Field(description = "This will contain the strategies of the competitors. It will be a string that describes the strategies in terms of product features, pricing, marketing strategies, or any other relevant metric.")
    key_insights: str = Field(description = "This will contain the key insights of the competitor analysis. It will be a string that summarizes the competitor analysis in terms of key findings, insights, and recommendations.")


class CustomerResearch(BaseModel):
    
    """This class defines the structure of Customer Research agent. It will conduct customer research mainly through the llm itself instead of web search and provide insights on customer needs, preferences, and behavior."""

    customer_needs: str = Field(description = "This will contain the needs of the customers. It will be a string that describes the needs in terms of product features, pricing, marketing strategies, or any other relevant metric.")
    customer_preferences: str = Field(description = "This will contain the preferences of the customers. It will be a string that describes the preferences in terms of product features, pricing, marketing strategies, or any other relevant metric.")
    customer_behavior: str = Field(description = "This will contain the behavior of the customers. It will be a string that describes the behavior in terms of product features, pricing, marketing strategies, or any other relevant metric.")
    key_insights: str = Field(description = "This will contain the key insights of the customer research. It will be a string that summarizes the customer research in terms of key findings, insights, and recommendations.")


class BuisnessModel(BaseModel):
    
    """This class defines the structure of Buisness Model agent. It will create a buisness model for the idea based on the insights provided by the other agents."""

    revenue_model: str = Field(description = "This will contain the revenue model of the idea. It will be a string that describes the revenue model in terms of pricing, sales channels, or any other relevant metric.")
    cost_structure: str = Field(description = "This will contain the cost structure of the idea. It will be a string that describes the cost structure in terms of fixed costs, variable costs, or any other relevant metric.")
    key_partners: str = Field(description = "This will contain the key partners of the idea. It will be a string that describes the key partners in terms of suppliers, distributors, or any other relevant metric.")
    key_activities: str = Field(description = "This will contain the key activities of the idea. It will be a string that describes the key activities in terms of production, marketing, or any other relevant metric.")
    key_resources: str = Field(description = "This will contain the key resources of the idea. It will be a string that describes the key resources in terms of human resources, financial resources, or any other relevant metric.")
    value_proposition: str = Field(description = "This will contain the value proposition of the idea. It will be a string that describes the value proposition in terms of product features, customer benefits, or any other relevant metric.")    
    key_insights: str = Field(description = "This will contain the key insights of the buisness model. It will be a string that summarizes the buisness model in terms of key findings, insights, and recommendations.")
    

class TechnicalArchitecture(BaseModel):

    """This class defines the structure of Technical Architecture agent. It will create a technical architecture for the idea based on the insights provided by the other agents."""

    architecture_diagram: str = Field(description = "This will contain the architecture diagram of the idea. It will be a string that describes the architecture diagram in terms of components, modules, or any other relevant metric.")
    technology_stack: str = Field(description = "This will contain the technology stack of the idea. It will be a string that describes the technology stack in terms of programming languages, frameworks, or any other relevant metric.")
    key_insights: str = Field(description = "This will contain the key insights of the technical architecture. It will be a string that summarizes the technical architecture in terms of key findings, insights, and recommendations.")
    feasibility: bool = Field(description = "This will contain the feasibility of the idea. It will be a boolean that describes whether the idea is feasible or not based on the technical architecture and technology stack.")

class RiskAnalysis(BaseModel):
    
    """This class defines the structure of Risk Analysis agent. It will create a risk analysis for the idea based on the insights provided by the other agents."""

    risk_identification: str = Field(description = "This will contain the risk identification of the idea. It will be a string that describes the risk identification in terms of potential risks, threats, or any other relevant metric.")
    risk_assessment: str = Field(description = "This will contain the risk assessment of the idea. It will be a string that describes the risk assessment in terms of likelihood, impact, or any other relevant metric.")
    risk_mitigation: str = Field(description = "This will contain the risk mitigation of the idea. It will be a string that describes the risk mitigation in terms of strategies, plans, or any other relevant metric.")
    key_insights: str = Field(description = "This will contain the key insights of the risk analysis. It will be a string that summarizes the risk analysis in terms of key findings, insights, and recommendations.")
    risk_acceptance: bool = Field(description = "This will contain the risk acceptance of the idea. It will be a boolean that describes whether the idea is acceptable or not based on the risk analysis and risk mitigation strategies.")

class pitchDeck(BaseModel):

    """This class defines the structure of Pitch Deck agent. It will create a pitch deck for the idea based on the insights provided by the other agents."""

    pitch_deck: str = Field(description = "This will contain the pitch deck of the idea. It will be a string that describes the pitch deck in terms of slides, content, or any other relevant metric.")
    key_insights: str = Field(description = "This will contain the key insights of the pitch deck. It will be a string that summarizes the pitch deck in terms of key findings, insights, and recommendations.")



class AgentState(TypedDict):

    """this class defines the state of the agent. It contains the following attributes:"""

    next_agent : str
    idea : str
    messages : Annotated[List[BaseMessage], add_messages]
    venture_manager_output : VentureManager
    market_research_output : MarketResearch
    competitor_analysis_output : CompetitorAnalysis
    customer_research_output : CustomerResearch
    buisness_model_output : BuisnessModel
    technical_architecture_output : TechnicalArchitecture
    risk_analysis_output : RiskAnalysis
    pitch_deck_output : pitchDeck


llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
venture_manager_llm = llm.with_structured_output(VentureManager)
market_research_llm = llm.with_structured_output(MarketResearch)
competitor_analysis_llm = llm.with_structured_output(CompetitorAnalysis)
customer_research_llm = llm.with_structured_output(CustomerResearch)
technical_architecture_llm = llm.with_structured_output(TechnicalArchitecture)
risk_analysis_llm = llm.with_structured_output(RiskAnalysis)
pitch_deck_llm = llm.with_structured_output(pitchDeck)
buisness_model_llm = llm.with_structured_output(BuisnessModel)











def VentureManagerAgent(state: AgentState):

    """This node will break down the idea of the user into smaller tasks and assign them to the relevant agents. It will use the VentureManager llm to generate the tasks for the other agents."""
    
    idea = state["idea"]

    prompt = f"You are a venture manager. You have to break down the idea of the user into smaller tasks and assign them to the relevant agents. The idea is: {idea}. Please provide the tasks for the following agents: Market Research Agent, Competitor Analysis Agent, Customer Research Agent. The output should be in the form of VentureManager model."

    output = venture_manager_llm.invoke([SystemMessage(content=prompt) , HumanMessage(content=idea)])

    return {"venture_manager_output": output}


def MarketResearchAgent(state: AgentState):

    task = state["venture_manager_output"].market_research

    system_prompt = """
    You are an expert Market Research Consultant.

    Your responsibility is to perform only the assigned market research task.

    Return the output strictly in the MarketResearch schema.
    """

    human_prompt = f"""
    Objective:
    {task.objective}

    Instructions:
    {task.instructions}
    """

    output = market_research_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)


]
    
)
    return {"market_research_output": output}

def CompetitorAnalysisAgent(state: AgentState):

    task = state["venture_manager_output"].competitor_analysis

    system_prompt = """
    You are an expert Competitor Analysis Consultant.

    Your responsibility is to perform only the assigned competitor analysis task.

    Return the output strictly in the CompetitorAnalysis schema.
    """

    human_prompt = f"""
    Objective:
    {task.objective}

    Instructions:
    {task.instructions}
    """

    output = competitor_analysis_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
]
    
)
    return {"competitor_analysis_output": output}
    
def CustomerResearchAgent(state: AgentState):

    task = state["venture_manager_output"].customer_research

    system_prompt = """
    You are an expert Customer Research Consultant.

    Your responsibility is to perform only the assigned customer research task.

    Return the output strictly in the CustomerResearch schema.
    """

    human_prompt = f"""
    Objective:
    {task.objective}

    Instructions:
    {task.instructions}
    """

    output = customer_research_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
]
   
)
    return {"customer_research_output": output}


def BuisnessModelAgent(state: AgentState):
    
    """This node will create a buisness model for the idea based on the insights provided by the other agents. It will use the BuisnessModel llm to generate the buisness model for the idea."""

    prompt = f"You are a buisness model agent. You have to create a buisness model for the idea based on the insights provided by the other agents. The insights are: Market Research: {state['market_research_output']}, Competitor Analysis: {state['competitor_analysis_output']}, Customer Research: {state['customer_research_output']}. Please provide the buisness model in the form of BuisnessModel model."

    output = buisness_model_llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="Create a buisness model for the idea based on the insights provided by the other agents.")
    ])

    return {"buisness_model_output": output}

def TechnicalArchitectureAgent(state: AgentState):
    
    """This node will create a technical architecture for the idea based on the insights provided by the other agents. It will use the TechnicalArchitecture llm to generate the technical architecture for the idea."""

    prompt = f"You are a technical architecture agent. You have to create a technical architecture for the idea based on the insights provided by the other agents. The insights are: Buisness Model: {state['buisness_model_output']}. Please provide the technical architecture in the form of TechnicalArchitecture model."

    output = technical_architecture_llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="Create a technical architecture for the idea based on the insights provided by the other agents.")
    ])

    return {"technical_architecture_output": output}

def RiskAnalysisAgent(state: AgentState):

    """This node will create a risk analysis for the idea based on the insights provided by the other agents. It will use the RiskAnalysis llm to generate the risk analysis for the idea."""

    prompt = f"You are a risk analysis agent. You have to create a risk analysis for the idea based on the insights provided by the other agents. The insights are: Technical Architecture: {state['technical_architecture_output']}. Please provide the risk analysis in the form of RiskAnalysis model."

    output = risk_analysis_llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="Create a risk analysis for the idea based on the insights provided by the other agents.")
    ])

    return {"risk_analysis_output": output}

def PitchDeckAgent(state: AgentState):
    
    """This node will create a pitch deck for the idea based on the insights provided by the other agents. It will use the PitchDeck llm to generate the pitch deck for the idea."""

    prompt = f"You are a pitch deck agent. You have to create a pitch deck for the idea based on the insights provided by the other agents. The insights are: Buisness Model: {state['buisness_model_output']}, Technical Architecture: {state['technical_architecture_output']}, Risk Analysis: {state['risk_analysis_output']}. Please provide the pitch deck in the form of PitchDeck model."

    output = pitch_deck_llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="Create a pitch deck for the idea based on the insights provided by the other agents.")
    ])

    return {"pitch_deck_output": output}










def RouteAfterTechnicalArchitecture(state: AgentState):

    """This function determines the route after the technical architecture agent. It will check the feasibility , if feasible then it will route to risk analysis agent else it will route to buisness model agent."""
    
    if state['technical_architecture_output'].feasibility:
        return 'risk_analysis'
    else:
        return 'Buisness_model'

def RouteAfterRiskAnalysis(state: AgentState):
    
    """This function determines the route after the risk analysis agent. It will check the risk acceptance , if accepted then it will route to pitch deck agent else it will route to buisness model agent."""
    
    if state['risk_analysis_output'].risk_acceptance:
        return 'pitch_deck'
    else:
        return 'Buisness_model'    







graph = StateGraph(AgentState)

# ---------------- Entry Point ----------------
graph.set_entry_point("venture_manager")

# ---------------- Nodes ----------------
graph.add_node("venture_manager", VentureManagerAgent)

graph.add_node("market_research", MarketResearchAgent)
graph.add_node("competitor_analysis", CompetitorAnalysisAgent)
graph.add_node("customer_research", CustomerResearchAgent)

graph.add_node("Business_model", BuisnessModelAgent)

graph.add_node("technical_architecture", TechnicalArchitectureAgent)
graph.add_node("risk_analysis", RiskAnalysisAgent)

graph.add_node("pitch_deck", PitchDeckAgent)

# ---------------- Phase 1 ----------------
graph.add_edge("venture_manager", "market_research")
graph.add_edge("venture_manager", "competitor_analysis")
graph.add_edge("venture_manager", "customer_research")

# ---------------- Phase 2 ----------------
graph.add_edge("market_research", "Business_model")
graph.add_edge("competitor_analysis", "Business_model")
graph.add_edge("customer_research", "Business_model")

# ---------------- Phase 3 ----------------
graph.add_edge("Business_model", "technical_architecture")

# Technical review decides whether to continue
graph.add_conditional_edges(
    "technical_architecture",
    RouteAfterTechnicalArchitecture,
    {
        "risk_analysis": "risk_analysis",
        "Business_model": "Business_model"
    }
)

graph.add_conditional_edges(
    "risk_analysis",
    RouteAfterRiskAnalysis,
    {
        "pitch_deck": "pitch_deck",
        "Business_model": "Business_model"
    }
)

# ---------------- Finish ----------------
graph.add_edge("pitch_deck", END)

agent = graph.compile()


def run_agent(idea: str):
    return agent.stream(
        {
            "idea": idea
        },
        stream_mode="updates"
    )

#print(result['venture_manager_output'])
#print(result["pitch_deck_output"])
#rint(result["risk_analysis_output"].risk_acceptance)