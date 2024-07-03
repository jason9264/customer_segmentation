import pandas as pd
import unittest

# Import your functions here
from src import function
# from function import assign_score, assign_value, assign_status, process_data

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            'test_1': {
                'income~both~salary/regular income-cat': 'MID',
                'Active_income~sum': 'VERY LOW',
                'income~bank~salary/regular income': 'HIGH',
                'bargain_groceries~sum': 'HIGH',
                'spend~both~discount stores': 'LOW',
                'bargain_personal/family': 'MID',
                'spend~both~bargain_discount_and_wholesale_stores': 'LOW',
                'Spend~both~mass_market_pet_services': 'MID',
                'premium_restaurants': 'HIGH',
                'premium_electronics/general_merchandise': 'MID',
                'spend~both~premium_department_stores': 'HIGH',
                'premium_travel': 'LOW',
                'elementary_middle_school~sum': 'LOW',
                'spend~card~child/dependent expenses': 'MID',
                'spend~both~primary and secondary schools': 'HIGH',
                'spend~bank~day care and preschools': 'LOW',
                'income~bank~children': 'HIGH',
                'income~bank~child support': 'LOW',
            },
            'test_2': {
                'income~both~salary/regular income-cat': 'LOW',
                'Active_income~sum': 'MID',
                'income~bank~salary/regular income': 'MID',
                'bargain_groceries~sum': 'VERY LOW',
                'spend~both~discount stores': 'HIGH',
                'bargain_personal/family': 'HIGH',
                'spend~both~bargain_discount_and_wholesale_stores': 'MID',
                'Spend~both~mass_market_pet_services': 'LOW',
                'premium_restaurants': 'LOW',
                'premium_electronics/general_merchandise': 'MID',
                'spend~both~premium_department_stores': 'HIGH',
                'premium_travel': 'VERY HIGH',
                'elementary_middle_school~sum': 'VERY HIGH',
                'spend~card~child/dependent expenses': 'VERY LOW',
                'spend~both~primary and secondary schools': 'LOW',
                'spend~bank~day care and preschools': 'HIGH',
                'income~bank~children': 'MID',
                'income~bank~child support': 'MID',
            },
            'test_3': {
                'income~both~salary/regular income-cat': 'HIGH',
                'Active_income~sum': 'HIGH',
                'income~bank~salary/regular income': 'LOW',
                'bargain_groceries~sum': 'LOW',
                'spend~both~discount stores': 'MID',
                'bargain_personal/family': 'LOW',
                'spend~both~bargain_discount_and_wholesale_stores': 'HIGH',
                'Spend~both~mass_market_pet_services': 'HIGH',
                'premium_restaurants': 'VERY HIGH',
                'premium_electronics/general_merchandise': 'HIGH',
                'spend~both~premium_department_stores': 'MID',
                'premium_travel': 'MID',
                'elementary_middle_school~sum': 'MID',
                'spend~card~child/dependent expenses': 'HIGH',
                'spend~both~primary and secondary schools': 'LOW',
                'spend~bank~day care and preschools': 'VERY HIGH',
                'income~bank~children': 'LOW',
                'income~bank~child support': 'HIGH',
            },
        }

    def test_process_data_assign_values(self):
        # Test process_data function for correct value assignments

        processed_data = function.process_data(self.sample_data)

        # Test specific cases
        self.assertEqual(processed_data['test_1']['Discretionary'], 'high')
        self.assertEqual(processed_data['test_1']['Family'], 'family')
        self.assertEqual(processed_data['test_1']['Income'], 'medium')        

        self.assertEqual(processed_data['test_2']['Discretionary'], 'medium')
        self.assertEqual(processed_data['test_2']['Family'], 'family')
        self.assertEqual(processed_data['test_2']['Income'], 'medium')

        self.assertEqual(processed_data['test_3']['Discretionary'], 'medium')
        self.assertEqual(processed_data['test_3']['Family'], 'family')
        self.assertEqual(processed_data['test_3']['Income'], 'high')
        
        
    def test_assign_score(self):
        # Test assign_score function

        # Test with valid input
        self.assertEqual(function.assign_score('MID'), 3)

        # Test with invalid input
        self.assertEqual(function.assign_score('INVALID_CATEGORY'), 0)

    def test_assign_value(self):
        # Test assign_value function

        # Test with valid input
        self.assertEqual(function.assign_value(1, 5), 'low')
        self.assertEqual(function.assign_value(3, 5), 'medium')
        self.assertEqual(function.assign_value(4, 5), 'high')

        # Test with invalid input
        self.assertEqual(function.assign_value(0, 5), 'low')
        self.assertIs(ValueError, function.assign_value(6, 5))
        try:
            function.assign_value(1, 0)
            self.fail()
        except(ZeroDivisionError):
            self.failureException(ZeroDivisionError)

    def test_assign_status(self):
        # Test assign_status function

        # Test with valid input
        self.assertEqual(function.assign_status(1, 5), 'individual')
        self.assertEqual(function.assign_status(3, 5), 'family')

        # Test with invalid input
        self.assertEqual(function.assign_status(0, 5), 'individual')
        try:
            function.assign_status(1, 0)
            self.fail()
        except(ZeroDivisionError):
            self.failureException(ZeroDivisionError)

    def test_process_data(self):
        # Test process_data function

        processed_data = function.process_data(self.sample_data)

        # Assert that processed_data is a dictionary
        self.assertIsInstance(processed_data, dict)

        # Assert that each test_1 in sample data is present in processed_data
        for test_1 in self.sample_data:
            self.assertIn(test_1, processed_data)

        # Assert that processed_data has expected structure
        for test_1, attributes in processed_data.items():
            # Assert that each test_1 has 'Income', 'Discretionary', and 'Family' keys
            self.assertIn('Discretionary', attributes)
            self.assertIn('Family', attributes)
            self.assertIn('Income', attributes)

            # Assert that values are within expected range or categories
            self.assertIn(attributes['Discretionary'], ('low', 'medium', 'high'))
            self.assertIn(attributes['Family'], ('individual', 'family'))
            self.assertIn(attributes['Income'], ('low', 'medium', 'high'))

    def test_evaluator(self):
        # Test evaluator function
        processed_data = function.process_data(self.sample_data)
        i_data = function.evaluator(processed_data, "individual")
        g_data = function.evaluator(processed_data, "group")

        # Assert that the different combinations of attributes from the sample data are in the output data
        # Individual
        self.assertIn("Mainstream Budgeting Families", i_data.keys())
        self.assertIn("Mainstream Lavish Families", i_data.keys())
        self.assertIn("Affluent Budgeting Families", i_data.keys())
        # Group
        self.assertIn("Mainstream Families", g_data.keys())
        self.assertIn("Affluent Families", g_data.keys())

        # Assert that each user from the sample data are in the output data
        # Individual
        self.assertIn('test_2', i_data["Mainstream Budgeting Families"])
        self.assertIn('test_1', i_data["Mainstream Lavish Families"])
        self.assertIn('test_3', i_data["Affluent Budgeting Families"])
        #G roup
        self.assertIn('test_2', g_data["Mainstream Families"])
        self.assertIn('test_1', g_data["Mainstream Families"])
        self.assertIn('test_3', g_data["Affluent Families"])
