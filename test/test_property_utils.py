# test/test_property_utils.py
from hypothesis import given, strategies as st
from data.utils import parse_answers

@given(
    st.text(),                   # any random Unicode string
    st.integers(min_value=1, max_value=50)
)
def test_parse_answers_never_crash(input_str, total_q):
    """
    No matter what random string or total_q you feed parse_answers, it should:
      - never raise an exception
      - return a list of exactly length total_q
    """
    result = parse_answers(input_str, total_q)
    # must be a list, length matches
    assert isinstance(result, list)
    assert len(result) == total_q

@given(
    st.lists(
        st.tuples(
            st.integers(min_value=1, max_value=10),
            st.sampled_from(["A","B","C","D"])
        ),
        min_size=1,
        max_size=10,
        unique_by=lambda x: x[0]  # ensure no duplicate question numbers
    )
)
def test_parse_answers_valid_pairs(pairs):
    """
    Generate valid tokens like '3.C', ensure parse_answers places them correctly.
    """
    total_q = 10
    tokens = [f"{num}.{letter}" for num, letter in pairs]
    input_str = " ".join(tokens)
    result = parse_answers(input_str, total_q)
    for num, letter in pairs:
        # token 'num.letter' must appear at index num-1
        assert result[num-1] == letter
