from playerstars_domain import PrivacyPolicy

rate = PrivacyPolicy(entity_id='id123', privacy_policy='oieoieoieoie')


def test_convert_star_rate():
    assert rate
    assert rate.from_json(rate.to_json())
