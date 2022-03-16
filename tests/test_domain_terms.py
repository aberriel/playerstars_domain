from playerstars_domain import Terms


rate = Terms(entity_id='id123', terms='oieoieoieoieoieoie')


def test_convert_star_rate():
    assert rate
    assert rate.from_json(rate.to_json())
