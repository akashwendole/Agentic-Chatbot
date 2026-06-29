from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from src.langgraphAgenticAI.states.state import State
from src.langgraphAgenticAI.nodes.bsaic_chatbot_node import BasicChatbotNode
from src.langgraphAgenticAI.tools.search_tool import get_tools, create_tool_node
from src.langgraphAgenticAI.nodes.chatbot_with_tool_node import ChatbotWithToolNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrates it into the graph. The Chatbot node is set as both the
        entry and exit point of the graph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("Chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "Chatbot")
        self.graph_builder.add_edge("Chatbot", END)

    def chatbot_with_tools_build_graph(self):
        """
        Build an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node
        and a tool node. It defines tools, initializes the chatbot with tool
        capabilities, and sets up conditional and direct edges between nodes.
        The chatbot node is set as the entry point.
        """
        ## Define the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)

        ## Define the LLM
        llm = self.llm

        ## Define the chatbot node
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

        ## Add nodes
        self.graph_builder.add_node("Chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        # Define conditional edges and direct edges
        self.graph_builder.add_edge(START, "Chatbot")
        self.graph_builder.add_conditional_edges("Chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "Chatbot")
        self.graph_builder.add_edge("Chatbot", END)

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Tool":
            self.chatbot_with_tools_build_graph()

        return self.graph_builder.compile()

    