import re

def filter_after_separator(input_list):
    # Pattern: matches strings like "(4)", "( 4 )", etc.
    pattern = re.compile(r'^\s*\(\s*\d{1,2}\s*\)\s*$')
    
    for i, item in enumerate(input_list):
        if pattern.match(item):
            return input_list[i+1:]
    
    # If no separator found, return original list
    return input_list

def run_tests():
    test_cases = [
        ([
        "Dokumer",
        "No. Paspor",
        "( 12 )"
    ], []),
        (['Tempat Lahir', '( 4 )', 'INDRAMAYU', 'INDRAMAYU'], ['INDRAMAYU', 'INDRAMAYU']),
        (['(4)', 'INDRAMAYU'], ['INDRAMAYU']),
        (['( 12 )', 'A', 'B', 'C'], ['A', 'B', 'C']),
        (['Tempat', 'Lahir', 'INDRAMAYU'], ['Tempat', 'Lahir', 'INDRAMAYU']),  # No separator
        (['(7)'], []),
        (['Foo', '( 99 )', 'Bar'], ['Bar']),
        (['(abc)', 'Test'], ['(abc)', 'Test']),  # Invalid separator, letters not allowed
        ([], []),
    ]
    
    for i, (input_data, expected_output) in enumerate(test_cases):
        result = filter_after_separator(input_list=input_data)
        assert result == expected_output, f"Test case {i+1} failed: expected {expected_output}, got {result}"
    
    print("All tests passed!")

run_tests()