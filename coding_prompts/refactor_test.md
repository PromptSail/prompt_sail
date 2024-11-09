


Please recommend the way how to organize and structure the tests that checks counting transations and costs logic, how to properly group, setup all necessary preliminary data, how to clean the database in  @test_file follow the best practises form @Pytest and @FastAPI documentation.

1. Check if all the test functions has proper names with the same naming pattern, propose the new names if needed:
    - test_<name>_<condition>_<expected_result> 
    - examples: 
        test_5min_duration_with_5min_granularity_returns_single_interval_with_tokens_and_costs
        test_30min_duration_with_5min_granularity_returns_six_intervals_with_tokens_and_costs

2. Check and propose the new docstrings if needed for all the test functions with the following structure,do not change the test name and test logic, focus only on docstring. Docstring format:
    - One line description that describes what the test case is about. Test name and description should be in sync.
    - Given: Some initial data that is needed to run the test.
    - When: Some action that is needed to run the test.
    - Then: Expected result of the test.
    Example:
    ''' 
    Tests token usage and cost statistics for a 5-minute time frame with 5-minute granularity.

    Given: Transactions spanning 5 minutes (2023-11-01 12:00-12:05)
    When: Requesting token and cost statistics with 5-minute granularity
    Then: Returns one interval with correct token counts and costs for each model
    ''' 
3. Review the test functions body and test names and try to group them into logical test cases, each test case should be a class, create new file for new test cases with suffix _refactored.py. Examples of Test Classes:
    - tests for counting transactions: TestCountTransactionsStatistics
    - tests for counting costs: TestCountCostsStatistics    
    - tests for checking costs logic: TestCheckCostsLogic
    - tests for checking transactions logic: TestCheckTransactionsLogic
4. Create the base class for all the test cases, extract all the common logic to the base class, setup all necessary data, clean the database after each test.

5. Review the new test cases, check if you do not miss any test method, compere original and refactored test files.
