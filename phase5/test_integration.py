import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Ensure the project root is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase3.logic import filter_restaurants
from phase4.groq_service import get_ai_recommendations

class TestZomatoAIIntegration(unittest.TestCase):
    
    def setUp(self):
        # Create a small mock dataframe for integration testing
        self.mock_df = pd.DataFrame({
            'name': ['Test Restaurant', 'Cheap Eats', 'Fancy Place'],
            'location': ['Bangalore', 'Bangalore', 'Mumbai'],
            'approx_cost(for two people)': [800, 300, 2000],
            'rate': ['4.1/5', '3.5/5', '4.8/5'],
            'cuisines': ['North Indian', 'Street Food', 'Fine Dining']
        })

    def test_full_logic_flow(self):
        """
        Integration test: Phase 3 (Filtering) -> Phase 4 (Mocked AI Recommendation)
        """
        user_prefs = {'location': 'Bangalore', 'budget': 500}
        
        # 1. Test Filtering Logic (Phase 3)
        filtered = filter_restaurants(self.mock_df, user_prefs['location'], user_prefs['budget'])
        
        self.assertEqual(len(filtered), 2)
        self.assertIn('Test Restaurant', filtered['name'].values)
        self.assertIn('Cheap Eats', filtered['name'].values)

    @patch('phase4.groq_service.Groq')
    def test_ai_service_integration(self, mock_groq):
        """
        Integration test: Verifying data reaches the AI service layer correctly.
        """
        # Mock Groq Client Response
        mock_client = MagicMock()
        mock_groq.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = "AI Recommendation: Try Test Restaurant!"
        
        user_prefs = {'location': 'Bangalore', 'budget': 500}
        
        # Filtered data
        filtered = self.mock_df[self.mock_df['location'] == 'Bangalore']
        
        # 2. Test AI Recommendation (Phase 4)
        with patch.dict('os.environ', {'GROQ_API_KEY': 'fake_key'}):
            response = get_ai_recommendations(filtered, user_prefs)
            self.assertEqual(response, "AI Recommendation: Try Test Restaurant!")

if __name__ == "__main__":
    unittest.main()
