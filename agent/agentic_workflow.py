from langgraph.graph import StateGraph, MessageState, END, START
from langgraph.prebuilt import ToolNode, tools_condition

from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT


class GraphBuilder():
    def __init__(self, model_provider: str = "groq"):
        self.tools=[]
        self.system_prompt = SYSTEM_PROMPT
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.graph = None


    def agent_function(self, state: MessageState):
        user_question = state["messages"]
        input_question = self.system_prompt + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {
            "messages": response,
            "tools": self.tools
        }

    def build_graph(self):
        graph_builder = StateGraph(MessageState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        """
        Build the agentic workflow graph.
        """
        print("Building agentic workflow graph...")
        return self.build_graph()
        



    


