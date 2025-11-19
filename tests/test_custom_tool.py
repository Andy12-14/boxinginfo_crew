import unittest
from unittest.mock import patch
from ai_boxing.src.ai_boxing.tools.custom_tool import BoxerProfileScrapeTool

class TestBoxerProfileScrapeTool(unittest.TestCase):
    @patch('ai_boxing.src.ai_boxing.tools.custom_tool.BoxerInfoScrapeTool._run')
    def test_boxer_profile_scrape_tool(self, mock_boxer_info_scrape_tool):
        # Mock the BoxerInfoScrapeTool to return a JSON string
        mock_boxer_info_scrape_tool.return_value = '''
        {
            "name": "Tyson Fury",
            "alias": "The Gypsy King",
            "age": "36",
            "nationality": "British",
            "sex": "male",
            "height": "6' 9'' / 206cm",
            "reach": "85'' / 216cm",
            "stance": "orthodox",
            "record": "34-1-1",
            "win": "34",
            "loss": "1",
            "draw": "1",
            "ko": "24",
            "KOs_percentage": "70.59%",
            "recent_fights": "loss to Oleksandr Usyk",
            "titles": "WBC World Heavy",
            "notable_achievements": "Lineal champion",
            "world_ranking": "2",
            "USA_ranking": null,
            "Bouts": "36",
            "Rounds": "221",
            "Career": "2008-2024",
            "Debut": "2008-12-06",
            "next_fight": "2024-12-21 vs Oleksandr Usyk"
        }
        '''

        # Create an instance of the tool
        tool = BoxerProfileScrapeTool()

        # Run the tool with a test boxer name
        result = tool._run(boxer_name="Tyson Fury")

        # Check that the output is a string
        self.assertIsInstance(result, str)

        # Check that the output contains the expected sections
        self.assertIn("Boxer Infos", result)
        self.assertIn("Boxing Highlights", result)

        # Check that the output contains the expected information
        self.assertIn("Name: Tyson Fury", result)
        self.assertIn("Alias: The Gypsy King", result)
        self.assertIn("Stance: orthodox", result)
        self.assertIn("Record: 34-1-1", result)

if __name__ == '__main__':
    unittest.main()
