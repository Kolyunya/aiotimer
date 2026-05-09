from pytest import approx, mark

from aiotimer.utility.boolean import coin_flip


@mark.flaky(retries=3)
def test_coin_flip() -> None:
    heads_count = 0
    tails_count = 0

    for _ in range(100):
        result = coin_flip()

        if result:
            heads_count += 1
        else:
            tails_count += 1

    assert heads_count == approx(tails_count, abs=25)
