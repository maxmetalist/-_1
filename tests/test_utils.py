

def test_filter_and_sort():
    test_data = [

    ]

    result = filter_transactions_by_current_month(test_data, "31.01.2023")


    assert len(result) == 3


def test_edge_cases():
    test_data = [

    ]

    result = filter_transactions_by_current_month(test_data, "31.01.2023")
    assert len(result) == 2
