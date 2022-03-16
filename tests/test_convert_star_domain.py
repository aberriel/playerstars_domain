from playerstars_domain import ConvertStarRate

rate = ConvertStarRate(entity_id='id123', convert_rate=3)


def test_convert_star_rate():
    assert rate
    assert rate.from_json(rate.to_json())
