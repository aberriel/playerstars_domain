from playerstars_domain import (
    ApiResponseInfo,
    Subscriber,
    Subscription)


def test_subscriber_post_params_new_vault():
    params_1 = Subscriber.post_params(True)
    assert params_1 == {'new_vault': 'true'}
    params_2 = Subscriber.post_params(False)
    assert params_2 == {'new_vault': 'false'}


def test_subscription_post_params_new_customer():
    params_1 = Subscription.post_params(True)
    assert params_1 == {'new_customer': 'true'}
    params_2 = Subscription.post_params(False)
    assert params_2 == {'new_customer': 'false'}


def test_api_response_info_from_json_alerts():
    response_info_json = {
        "alerts": [{
            "code": "MA76",
            "description": "O CEP do endereço deve ter apenas dígitos "
                           "numéricos. Os demais caracteres foram ignorados"
        }],
        "message": "Cliente criado com sucesso"
    }
    response_info = ApiResponseInfo.from_json(response_info_json)
    assert response_info
    assert len(response_info.errors) == 0
    assert len(response_info.alerts) == 1
    assert response_info.message == 'Cliente criado com sucesso'


def test_api_response_info_fron_json_errors():
    response_info_json = {
        "errors": [{
            "code": "MA6",
            "description": "Código do plano já utilizado. Escolha outro código"
        }]
    }
    response_info = ApiResponseInfo.from_json(response_info_json)
    assert response_info
    assert len(response_info.alerts) == 0
    assert len(response_info.errors) == 1
    assert response_info.errors[0].code == 'MA6'
