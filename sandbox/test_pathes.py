from hacka.games.moveit import GameEngine
import bot

def test_gamemaster_distances_path():
    game= GameEngine(
        matrix= [
            [00, 00, 00, 00],
            [-1, 00, -1, -1],
            [00, 00, 00, 00],
            [00, -1, -1, 00]
        ],
        tic= 10, missions= [(4, 5), (7, 8)] )
    myBot= bot.VoidBot()
    myBot.wakeUp( 1, 1, game.asPod() )

    assert myBot._model.map().size() == 11
    assert myBot._distances == [
        [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        [ 1, 0, 1, 2, 3, 2, 4, 3, 4, 5,  5,  6],
        [ 2, 1, 0, 1, 2, 1, 3, 2, 3, 4,  4,  5],
        [ 3, 2, 1, 0, 1, 2, 4, 3, 4, 5,  5,  6],
        [ 4, 3, 2, 1, 0, 3, 5, 4, 5, 6,  6,  7],
        [ 5, 2, 1, 2, 3, 0, 2, 1, 2, 3,  3,  4],
        [ 6, 4, 3, 4, 5, 2, 0, 1, 2, 3,  1,  4],
        [ 7, 3, 2, 3, 4, 1, 1, 0, 1, 2,  2,  3],
        [ 8, 4, 3, 4, 5, 2, 2, 1, 0, 1,  3,  2],
        [ 9, 5, 4, 5, 6, 3, 3, 2, 1, 0,  4,  1],
        [10, 5, 4, 5, 6, 3, 1, 2, 3, 4,  0,  5],
        [11, 6, 5, 6, 7, 4, 4, 3, 2, 1,  5,  0]
    ]

    assert myBot.moveToward(1, 2) == (3, 2)
    assert myBot.moveToward(4, 4) == (0, 4)
    assert myBot.moveToward(5, 11) == (6, 7)

    assert myBot.path(1, 11) == (
        [3, 6, 6, 3, 3, 6],
        [2, 5, 7, 8, 9, 11]
    )
