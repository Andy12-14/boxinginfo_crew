from crewai_tools import ScrapegraphScrapeTool
from crewai.tools import BaseTool
from typing import Type, Optional, Any
from pydantic import BaseModel, Field
import pywhatkit
from urllib.parse import urlparse, urljoin
from ddgs import DDGS
import json
import os
# get boxer_name from user input in main.py
# i want to import ScrapegraphScrape API key from .env file
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
SCRAPEGRAPH_API_KEY = os.getenv("SCRAPEGRAPH_API_KEY")


# optional imports for fetching and parsing HTML


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
    

class SearchToolInput1(BaseModel):
    """Input schema for SearchTool.

    This tool expects the user's `boxer_name` input from `main.py` to be passed in
    via CrewAI input interpolation (use `{boxer_name}` in your task/agent config).
    """
    boxer_name: Any = Field(..., description="The boxer name to look up (from main.py inputs ).")
    url1: Any = Field("https://boxrec.com/en/", description="The website URL to search for information about boxer.")
class SearchTool1(BaseTool):
    name: str = "Web Search Tool1"
    description: str = (
        "Search for information on specified websites. Use this to find the latest news and details about boxers and return the results."
    )
    args_schema: Type[BaseModel] = SearchToolInput1

    def _run(self, boxer_name: str, url1: str = "https://boxrec.com/en/") -> str:
        # The boxer_name should come from CrewAI inputs via `{boxer_name}` interpolation.
        # If caller passed a metadata dict (from LLM) prefer BOXER_NAME env var if set
        if not boxer_name or not isinstance(boxer_name, str):
            env_name = os.getenv("BOXER_NAME")
            if env_name and isinstance(env_name, str):
                boxer_name = env_name
            else:
                return "No boxer name provided. Ensure `boxer_name` is passed from main.py via inputs."

        print(f"Searching for BoxRec profile URL for: {boxer_name}")
        ddgs = DDGS()
        results = ddgs.text(
            query=f"{boxer_name} BoxRec",
            region="us-en",
            max_results=5,
            safesearch="moderate"
        )
        boxrec_url = None
        for result in results:
            if result.get('href') and "boxrec.com" in result['href']:
                boxrec_url = result['href']
                break

        if boxrec_url:
            print(f"Found BoxRec profile URL: {boxrec_url}")
        else:
            print("BoxRec profile URL not found in the top search results.")

        return boxrec_url

scrape_tool = None  # Will be initialized at runtime with the correct boxer_name

class SearchToolInput2(BaseModel):
    """Input schema for SearchTool2.

    Accepts flexible input shapes; the tool will coerce to strings at runtime.
    """
    query2: Any = Field("latest boxing news", description="The search query to look up information.")
    url2: Any = Field("https://www.espn.com/boxing/", description="The website URL to search for information about boxing.")


class SearchTool2(BaseTool):
    name: str = "Web Search Tool2"
    description: str = (
        "Search for information on the specified ESPN boxing page and return the top results. "
        "This avoids scraping private data and returns public headlines, URLs and short snippets."
    )
    args_schema: Type[BaseModel] = SearchToolInput2

    def _run(self, query2: Any = "latest boxing news", url2: Any = "https://www.espn.com/boxing/") -> str:
        # coerce inputs
        def _coerce_to_str(val: Any) -> str:
            if isinstance(val, str):
                return val
            if isinstance(val, dict):
                for k in ("value", "description", "default", "text", "query", "query2"):
                    if k in val and isinstance(val[k], str):
                        return val[k]
                for v in val.values():
                    if isinstance(v, str):
                        return v
                return str(val)
            try:
                return str(val)
            except Exception:
                return ""

        query2_s = _coerce_to_str(query2).strip() or "latest boxing news"
        url2_s = _coerce_to_str(url2).strip() or "https://www.espn.com/boxing/"

        # use Scrapegraph API to summarize latest news at the provided URL
        scrape_tool2 = ScrapegraphScrapeTool(
            website_url=url2_s,
            user_prompt=(f"Take the latest 10 news articles about boxing from {url2_s} and provide a short summary of each, "
                         f"focused on the query: '{query2_s}'."),
            api_key=SCRAPEGRAPH_API_KEY
        )
        result = scrape_tool2.run()
        # Ensure a string is returned (tools may return dicts/lists)
        if isinstance(result, str):
            return result
        try:
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception:
            return str(result)
    
class BoxerScrapeInput(BaseModel):
    """Input schema for scraping boxer profiles."""
    boxer_name: Any = Field(..., description="The name of the boxer to get information about.")


class BoxerScrapeTool(BaseTool):
    name: str = "Boxer Scrape Tool"
    description: str = (
        "Given a boxer name, finds the BoxRec profile URL using DDGS, then uses ScrapegraphScrapeTool "
        "to extract structured information from the profile page. Returns the extracted info as a JSON object."
    )
    args_schema: Type[BaseModel] = BoxerScrapeInput

    def _run(self, boxer_name: Any) -> str:
        # Coerce boxer_name to a plain string if the agent passed a dict-like argument
        if isinstance(boxer_name, dict):
            boxer_name = boxer_name.get("boxer_name", "")
        
        # Step 1: Find BoxRec profile URL
        ddgs = DDGS()
        results = ddgs.text(
            query=f"{boxer_name} BoxRec",
            region="us-en",
            max_results=5,
            safesearch="moderate"
        )
        boxrec_url = None
        for result in results:
            if result.get('href') and "boxrec.com" in result['href']:
                boxrec_url = result['href']
                break

        if not boxrec_url:
            return f"Could not find BoxRec profile for '{boxer_name}'."

        # Step 2: Scrape the profile page
        try:
            scrape_tool = ScrapegraphScrapeTool(
                website_url=boxrec_url,
                user_prompt=(
                    'Extract the following information about the boxer and return it as a JSON object: '
                    '"name", "alias", "age", "nationality", "sex", "height", "reach", "record", "upcoming_fight", "division", '
                    '"world_ranking", "USA_ranking", "Bouts", "Rounds", "KOs", "Career", "Debut", "stance", "win", "loss", "draw", "ko", "KOs_percentage", "recent_fights", "titles", "notable_achievements", "next_fight"'
                ),
                api_key=SCRAPEGRAPH_API_KEY
            )
            result = scrape_tool.run()
            if isinstance(result, dict):
                return json.dumps(result)
            return result
        except Exception as e:
            return f"Failed to scrape BoxRec profile: {e}"


class SummarizeToolInput(BaseModel):
    """Input schema for SummarizeTool."""
    boxer_json_data: str = Field(..., description="The JSON data for the boxer. This should be the output of the BoxerScrapeTool.")
    news_json_data: str = Field(..., description="The JSON data for the news. This should be the output of the Web Search Tool2.")

class SummarizeTool(BaseTool):
    name: str = "Summarizer Tool"
    description: str = (
        "Parses JSON objects containing boxer information and news, and creates a human-readable summary. "
        "Use this to process the output of BoxerScrapeTool and Web Search Tool2 before sending it to the user."
    )
    args_schema: Type[BaseModel] = SummarizeToolInput

    def _run(self, boxer_json_data: str, news_json_data: str) -> str:
        try:
            boxer_data = json.loads(boxer_json_data)
            
            # Extract key information, handling missing keys gracefully
            name = boxer_data.get("name", "N/A")
            alias = boxer_data.get("alias", "N/A")
            age = boxer_data.get("age", "N/A")
            nationality = boxer_data.get("nationality", "N/A")
            record = boxer_data.get("record", "N/A")
            division = boxer_data.get("division", "N/A")
            stance = boxer_data.get("stance", "N/A")
            kos = boxer_data.get("ko", "N/A")
            
            summary = (
                f"Here is a summary for boxer {name} (Alias: {alias}):\n"
                f"- Age: {age}\n"
                f"- Nationality: {nationality}\n"
                f"- Stance: {stance}\n"
                f"- Division: {division}\n"
                f"- Record: {record}\n"
                f"- KOs: {kos}\n"
            )
            
            upcoming_fight = boxer_data.get("upcoming_fight")
            if upcoming_fight:
                summary += f"\nUpcoming Fight:\n{upcoming_fight}\n"

            recent_fights = boxer_data.get("recent_fights")
            if recent_fights:
                summary += "\nRecent Fights:\n"
                if isinstance(recent_fights, list):
                    for fight in recent_fights[:3]: # Limit to 3 recent fights
                        opponent = fight.get('opponent', 'N/A')
                        result = fight.get('result', 'N/A')
                        date = fight.get('date', 'N/A')
                        summary += f"- vs {opponent} on {date}: {result}\n"
                elif isinstance(recent_fights, str):
                    summary += f"- {recent_fights}\n"

            summary += "\n--- Latest Boxing News ---\n"
            try:
                news_data = json.loads(news_json_data)
                if isinstance(news_data, dict):
                    # It might be a single summary string inside a dict
                    if 'summary' in news_data:
                         summary += news_data['summary']
                    # Or it might be a list of articles
                    elif 'articles' in news_data and isinstance(news_data['articles'], list):
                        for article in news_data['articles'][:5]: # top 5 news
                            title = article.get('title', 'No Title')
                            link = article.get('link', '')
                            snippet = article.get('snippet', 'No summary available.')
                            summary += f"\n- {title} ({link}):\n  {snippet}\n"
                    else: # if it is a dictionary but not in the format we expect, we just dump it
                        summary += json.dumps(news_data, indent=2)

                elif isinstance(news_data, list):
                     for item in news_data[:5]: # top 5 news
                        if isinstance(item, dict):
                            title = item.get('title', 'No Title')
                            link = item.get('link', '')
                            snip = item.get('snippet', 'No summary available.')
                            summary += f"\n- {title} ({link}):\n  {snip}\n"
                        else:
                            summary += f"- {str(item)}\n"
                else: # if it's just a string
                    summary += news_json_data

            except (json.JSONDecodeError, TypeError):
                # If news is not a valid JSON, just append it as a string.
                summary += news_json_data

            return summary

        except json.JSONDecodeError:
            return "Invalid JSON data provided for the boxer. Could not summarize."
        except Exception as e:
            return f"An error occurred while summarizing the data: {e}"