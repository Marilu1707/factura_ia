import pytest
from unittest.mock import MagicMock, patch
import analytics.ai as ai_module


def make_mock_response(content: str):
    mock = MagicMock()
    mock.choices[0].message.content = content
    return mock


def test_predict_sales_retorna_texto():
    with patch.object(ai_module, "_client") as mock_client:
        mock_client.chat.completions.create.return_value = make_mock_response(
            "Las ventas muestran tendencia alcista para el próximo trimestre."
        )
        from analytics.ai import predict_sales
        result = predict_sales("Resumen: 47 facturas, $158k total en abril 2026")

    assert isinstance(result, str)
    assert len(result) > 0


def test_predict_sales_llama_openai_con_prompt():
    with patch.object(ai_module, "_client") as mock_client:
        mock_client.chat.completions.create.return_value = make_mock_response("ok")
        from analytics.ai import predict_sales
        predict_sales("mi prompt de prueba")

    call_args = mock_client.chat.completions.create.call_args
    messages = call_args.kwargs["messages"]
    assert messages[0]["role"] == "user"
    assert "mi prompt de prueba" in messages[0]["content"]


def test_detect_irregularities_retorna_texto():
    with patch.object(ai_module, "_client") as mock_client:
        mock_client.chat.completions.create.return_value = make_mock_response(
            "No se detectaron anomalías significativas."
        )
        from analytics.ai import detect_irregularities
        result = detect_irregularities("ventas: [100, 200, 5000, 150]")

    assert isinstance(result, str)
    assert len(result) > 0


def test_predict_sales_sin_openai_retorna_mensaje():
    import analytics.ai as ai_module
    original = ai_module._client
    ai_module._client = None
    try:
        result = ai_module.predict_sales("cualquier prompt")
    finally:
        ai_module._client = original

    assert isinstance(result, str)
    assert "not available" in result.lower()
