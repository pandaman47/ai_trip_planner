## front end streamlit app
from fastapi import FastAPI
from pydantic import BaseModel, Field
from agent.agentic_workflow import GraphBuilder
from utils.model_loader import ModelLoader
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        """
        Endpoint to query the travel planner agent.
        """
        print(f"Received query: {query.query}")
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph built and saved as 'my_graph.png' in {os.get_cwd()}")

        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)
        print(f"Output from agent: {output}")

        # if result is dict from agent with messages and tools
        if isinstance(output, dict) and "messages" in output:
            response = output["messages"][-1].content
        else:
            response = str(output)

        return {
            "response": response}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred: {str(e)}"}
            )