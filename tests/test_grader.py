from benchmark.grader import grade_task, numeric_pass, tools_pass


def test_numeric_pass_formats():
    assert numeric_pass("The tax is 8,100.00 dollars", 8100)
    assert numeric_pass("Total: 15000", 15000)


def test_tools_pass():
    assert tools_pass(["sql_query", "calculator"], ["sql_query", "calculator", "sql_query"])
    assert not tools_pass(["knowledge_search"], ["sql_query"])


def test_grade_task_combined():
    task = {
        "expected_contains": ["GOVERN"],
        "expected_numeric": 100,
        "required_tools": ["sql_query", "knowledge_search"],
    }
    ok = grade_task(task, "Revenue 100. GOVERN function.", ["sql_query", "knowledge_search"])
    assert ok["pass"]
