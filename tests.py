import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title_raises_exception():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points_limits():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_question_with_invalid_points_raises_exception():
    with pytest.raises(Exception):
        Question(title='Invalid points', points=0)
    with pytest.raises(Exception):
        Question(title='Invalid points', points=101)

def test_create_question_with_non_positive_max_selections_does_not_raise_exception():
    q0 = Question(title='Too many selections', max_selections=0)
    assert q0.max_selections == 0
    qneg = Question(title='Negative selections', max_selections=-1)
    assert qneg.max_selections == -1

def test_add_choice_appends_to_questions():
    question = Question(title='q1')
    question.add_choice('a', False)
    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_multiple_choices():
    question = Question(title='Test multiple choices')
    question.add_choice('Choice A', True)
    question.add_choice('Choice B', False)
    assert len(question.choices) == 2

def test_remove_choice_by_id_removes_correct_choice():
    question = Question(title='Remove choice')
    c = question.add_choice('To remove', False)
    question.remove_choice_by_id(c.id)
    assert len(question.choices) == 0

def test_remove_choice_by_invalid_id_raises_exception():
    question = Question(title='Remove choice invalid')
    question.add_choice('Valid choice', False)
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_select_choices_with_correct_ids_returns_only_correct():
    question = Question(title='Select correct', max_selections=2)
    c1 = question.add_choice('Right', True)
    c2 = question.add_choice('Wrong', False)
    selected = question.select_choices([c1.id, c2.id])
    assert selected == [c1.id]

def test_select_choices_exceeding_max_selections_raises_exception():
    question = Question(title='Exceed selections', max_selections=1)
    c1 = question.add_choice('A', False)
    c2 = question.add_choice('B', True)
    with pytest.raises(Exception):
        question.select_choices([c1.id, c2.id])

def test_set_correct_choices_marks_specified_choices():
    question = Question(title='Set correct')
    c1 = question.add_choice('A', False)
    c2 = question.add_choice('B', False)
    question.set_correct_choices([c2.id])
    assert c2.is_correct and not c1.is_correct

def test_add_choice_exceeding_text_limit_raises_exception():
    question = Question(title='Long text')
    with pytest.raises(Exception):
        question.add_choice('a' * 101, False)

def test_add_choice_with_empty_text_raises_exception():
    question = Question(title='Empty text')
    with pytest.raises(Exception):
        question.add_choice('', True)