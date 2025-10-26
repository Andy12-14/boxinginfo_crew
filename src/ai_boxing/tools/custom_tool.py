from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pywhatkit

# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")

# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, your agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."

class WhatsAppToolInput(BaseModel):
    """Input schema for WhatsAppTool."""
    message: str = Field(..., description="The message to send to the user via WhatsApp.It should be the report from the reporter agent")
    country_code: str = Field(..., description="The country code of the user's phone number, e.g., '1' for USA.")
    phone_number: str = Field(..., description="The user's phone number without the country code.")

class WhatsAppTool(BaseTool):
    name: str = "WhatsApp Message Tool"
    description: str = (
        "Send a WhatsApp message to the specified user. Use this to notify the user with news or reports about the desired boxer. "
        "The user must provide their WhatsApp number in international format."
    )
    args_schema: Type[BaseModel] = WhatsAppToolInput

    def _run(self, message: str, country_code: str, phone_number: str) -> str:
        try:
            full_number = f"+{country_code}{phone_number}"
            pywhatkit.sendwhatmsg_instantly(full_number, message)
            return f"Message sent to {full_number} via WhatsApp."
        except Exception as e:
            return f"Failed to send WhatsApp message: {e}"
        l
    
        
class SearchToolInput(BaseModel):
    """Input schema for SearchTool."""
    query: str = Field("latest boxing news" , description="The search query to look up information.")
    url1 : str= Field("https://ringmagazine.com/en", description="The website URL to search for information about boxing.")
    url2 : str= Field("https://boxrec.com/en/", description="The website URL to search for information about boxer.")
class SearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = (
        "Search for information on specified websites. Use this to find the latest news and details about boxing and boxers."
    )
    args_schema: Type[BaseModel] = SearchToolInput

    def _run(self, query: str, url1: str = "https://ringmagazine.com/en", url2: str = "https://boxrec.com/en/") -> str:
        try:
            # Use duckduckgo-search or similar to get actual results
            # For now return sample boxing info to test the flow
            if "Gervonta Davis" in query:
                return """
                Gervonta "Tank" Davis (29-0, 27 KOs):
                - Current WBA Lightweight Champion
                - Former IBF Super Featherweight Champion
                - Known for explosive power and speed
                - Last fight: TKO victory over Ryan Garcia in April 2023
                - Next potential opponent: discussions ongoing for early 2024
                
                Recent News:
                - Continues undefeated streak
                - Ranked #1 in lightweight division
                - Training camp updates show impressive form
                """
            return f"Found information about {query} in boxing databases. Please specify a boxer name for detailed information."
        except Exception as e:
            return f"Failed to perform web search: {e}"