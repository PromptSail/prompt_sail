from datetime import datetime
import pytest
from test_utils import read_transactions_with_prices_from_csv




class TestBasePortfolio:
    @pytest.fixture(autouse=True)
    def setup(self, client, application):
        self.client = client
        self.application = application
        
        self.header = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
        }
        
        
        with self.application.transaction_context() as ctx:
            repo = ctx["transaction_repository"]
            repo.delete_cascade(project_id="project-test")
            
            config = self.application['config']
            
            transactions = read_transactions_with_prices_from_csv(
                "test_transactions_tokens_cost_speed.csv",
                config.PRICE_LIST_PATH
            )
            for transaction in transactions:
                repo.add(transaction)
        
        yield
        
        # Clean up test data
        # with self.application.transaction_context() as ctx:
        #     repo = ctx["transaction_repository"]
        #     repo.delete_cascade(project_id="project-test")
    

        

class TestPortfolioCostsByTagAPIContract(TestBasePortfolio):
    """Tests for API contract in portfolio costs by tag statistics. Check for errors and invalid parameters and contract for returned data."""
    def make_costs_by_tag_request(self, period, date_from, date_to):
        """Helper method to make API request for portfolio statistics."""
        
        if date_from is None:
            date_from = ""
        if date_to is None:
            date_to = ""    
        
        api_url = f"/api/portfolio/costs_by_tag?"
        #create api url add parameters if they are not empty

        if period != "":
            api_url += f"period={period}"
        if date_from != "":
            api_url += f"&date_from={date_from}"
        if date_to != "":
            api_url += f"&date_to={date_to}"
        

        return self.client.get(
            api_url,
            headers=self.header,
        )
        
    def test_costs_by_tag_check_contract(self):
        """Tests costs by tag. Check the contract fields for returned data."""
        
        
        
        date_from = "2023-11-01T00:00:00"
        date_to = "2023-11-02T00:00:00"
        
        response = self.make_costs_by_tag_request(
            "day", 
            date_from, 
            date_to
        )
        
        resp_data = response.json()
        
        expected_dates = [ datetime.fromisoformat(date_from), 
                           datetime.fromisoformat(date_to),
        ]
        
        response_dates = [ datetime.fromisoformat(resp_data[0]['date']), 
                           datetime.fromisoformat(resp_data[1]['date'])
        ]
        
        assert response.status_code == 200
        
        assert len(resp_data) == 2
        assert response_dates == expected_dates
        assert len(resp_data[0]['records']) == 2
        assert len(resp_data[1]['records']) == 2
        
        records_0 = resp_data[0]['records']
        records_1 = resp_data[1]['records']
        
        # check the contract of the first record, if all fields are present and have correct types: tag, total_input_tokens, total_output_tokens, input_cumulative_total, output_cumulative_total, total_cost, total_transactions
        
        assert records_0[0]['tag'] == 'tag-0'
        assert records_0[0]['total_input_tokens'] == 1143
        assert records_0[0]['total_output_tokens'] == 6474
        assert records_0[0]['input_cumulative_total'] == 1143
        assert records_0[0]['output_cumulative_total'] == 6474
        assert records_0[0]['total_cost'] == pytest.approx(0.0313251, rel=1e-4)
        assert records_0[0]['total_transactions'] == 14
        
        # check the contract of the second record
        assert records_0[1]['tag'] == 'tag-1'
        assert records_0[1]['total_input_tokens'] == 1220   
        assert records_0[1]['total_output_tokens'] == 4379
        assert records_0[1]['input_cumulative_total'] == 1220
        assert records_0[1]['output_cumulative_total'] == 4379
        assert records_0[1]['total_cost'] == pytest.approx(0.0483646, rel=1e-4)
        assert records_0[1]['total_transactions'] == 15
        
        
        
        #check the contract of the second date 
        assert records_1[0]['tag'] == 'tag-0'
        assert records_1[0]['total_input_tokens'] == 0
        assert records_1[0]['total_output_tokens'] == 0
        assert records_1[0]['input_cumulative_total'] == 1143
        assert records_1[0]['output_cumulative_total'] == 6474
        assert records_1[0]['total_cost'] == pytest.approx(0, rel=1e-4)
        assert records_1[0]['total_transactions'] == 0
        
        assert records_1[1]['tag'] == 'tag-1'
        assert records_1[1]['total_input_tokens'] == 0
        assert records_1[1]['total_output_tokens'] == 0
        assert records_1[1]['input_cumulative_total'] == 1220
        assert records_1[1]['output_cumulative_total'] == 4379
        assert records_1[1]['total_cost'] == pytest.approx(0, rel=1e-4)
        assert records_1[1]['total_transactions'] == 0
        
        
        

