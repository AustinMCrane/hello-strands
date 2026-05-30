from strands_evals import Case

EVAL_CASES: list[Case] = [
    Case(name="basic", input="How many times does the letter 'l' appear in 'hello world'?", expected_output="3"),
    Case(name="no-match", input="Count 'z' in 'xylophone'", expected_output="0"),
    Case(name="case-sensitive", input="How many lowercase 'h' are in 'Hello Hello'?", expected_output="0"),
    Case(name="high-freq", input="Count 's' in 'mississippi'", expected_output="4"),
    Case(name="single-char", input="How many 'a' in 'a'?", expected_output="1"),
    Case(name="spaces", input="Count the spaces in 'hello world'", expected_output="1"),
    Case(name="natural-phrasing", input="In 'banana', how often does 'a' occur?", expected_output="3"),
    Case(name="special-chars", input="Count '!' in 'hello! world!'", expected_output="2"),
]
