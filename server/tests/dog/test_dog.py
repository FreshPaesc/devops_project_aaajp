import pytest
from server.py.dog import Dog, Card, Marble, PlayerState, Action, GameState, GamePhase



def test_swap_cards():
    pass # DA-34


@pytest.fixture
def game():
    return Dog()

def test_initialize_game():
    """Test initializing the Dog game."""
    game = Dog()
    state = game.get_state()
    assert state is not None
    assert len(state.list_player) == 4
    assert state.phase == GamePhase.RUNNING
    assert state.cnt_round == 1

def test_initial_game_state_values(game):
    """Test 001: Validate values of initial game state (cnt_round=1) [5 points]"""
    state = game.get_state()

    assert state.phase == GamePhase.RUNNING, f'{state}Error: "phase" must be GamePhase.RUNNING initially'
    assert state.cnt_round == 1, f'{state}Error: "cnt_round" must be 1 initially'
    assert len(state.list_card_discard) == 0, f'{state}Error: len("list_card_discard") must be 0 initially'
    assert len(state.list_card_draw) == 86, f'{state}Error: len("list_card_draw") must be 86 initially'
    assert len(state.list_player) == 4, f'{state}Error: len("list_player") must be 4'
    assert state.idx_player_active >= 0, f'{state}Error: "idx_player_active" must be >= 0'
    assert state.idx_player_active < 4, f'{state}Error: "idx_player_active" must be < 4'
    assert state.idx_player_started == state.idx_player_active, f'{state}Error: "idx_player_active" must be == "idx_player_started"'
    assert state.card_active is None, f'{state}Error: "card_active" must be None'
    assert not state.bool_card_exchanged, f'{state}Error: "bool_card_exchanged" must be False'

    for player in state.list_player:
        assert len(player.list_card) == 6, f'{state}Error: len("list_player.list_card") must be 6 initially'
        assert len(player.list_marble) == 4, f'{state}Error: len("list_player.list_marble") must be 4 initially'

def test_starting_player_is_active(game):
    """Test 002: Verify that the correct player starts the game [5 points]"""
    state = game.get_state()
    assert 0 <= state.idx_player_started < 4, f'{state}Error: "idx_player_started" must be in range (0-3)'
    assert state.idx_player_active == state.idx_player_started, f'{state}Error: "idx_player_active" must be equal to "idx_player_started" initially'

def test_set_custom_game_state():
    """Test 003: Set and validate a custom game state [5 points]"""
    game = Dog()
    new_state = GameState(
        cnt_player=4,
        phase=GamePhase.RUNNING,
        cnt_round=2,
        bool_card_exchanged=True,
        idx_player_started=1,
        idx_player_active=2,
        list_player=[
            PlayerState(name="Player 1", list_card=[], list_marble=[Marble(pos=None, is_save=False) for _ in range(4)]),
            PlayerState(name="Player 2", list_card=[], list_marble=[Marble(pos=None, is_save=False) for _ in range(4)]),
            PlayerState(name="Player 3", list_card=[], list_marble=[Marble(pos=None, is_save=False) for _ in range(4)]),
            PlayerState(name="Player 4", list_card=[], list_marble=[Marble(pos=None, is_save=False) for _ in range(4)])
        ],
        list_card_draw=[],
        list_card_discard=[],
        card_active=None
    )

    game.set_state(new_state)
    state = game.get_state()

    assert state.cnt_round == 2, f'{state}Error: "cnt_round" must be 2'
    assert state.idx_player_active == 2, f'{state}Error: "idx_player_active" must be 2'

def test_initial_marble_positions(game):
    """Test 004: Validate initial positions of all marbles [5 points]"""
    state = game.get_state()
    for player in state.list_player:
        for marble in player.list_marble:
            assert marble.pos is None, f'{state}Error: "marble.pos" must be None initially'
            assert not marble.is_save, f'{state}Error: "marble.is_save" must be False initially'

def test_initial_card_draw_pile(game):
    """Test 005: Validate the number of cards in the draw pile after initial deal [5 points]"""
    state = game.get_state()
    assert len(state.list_card_draw) == 86, f'{state}Error: "list_card_draw" must contain 86 cards initially'

def test_number_of_cards_in_round_2():
    """Test 047: Validate number of cards dealt in Round 2 [5 points]"""
    # Initialize the game
    game = Dog()
    # Manually set up the game to round 2
    game.next_turn()  # Simulate turns until a new round starts
    # Set up next round (should be round 2)
    while game.get_state().cnt_round == 1: # reapeate for 3, 4, 5, 6
        game.next_turn()
    # Now we're in round 2, verify that each player has 5 cards
    state = game.get_state()
    for player in state.list_player:
        # reapeate for 3 -> 4, 4 -> 3, 5 -> 2, 6-> 6
        assert len(player.list_card) == 5, f'Error: Expected 5 cards in round 2, found {len(player.list_card)}'