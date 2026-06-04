from unittest.mock import MagicMock, patch


def test_create_agent_reads_env_vars():
    env = {
        "OPENAI_BASE_URL": "https://test.example.com/v1",
        "OPENAI_API_KEY": "test-key",
        "MODEL_ID": "test-model",
    }
    with patch.dict("os.environ", env):
        with patch("hello_strands.agent.OpenAIModel") as mock_model_cls:
            with patch("hello_strands.agent.Agent") as mock_agent_cls:
                mock_model_cls.return_value = MagicMock()
                mock_agent_cls.return_value = MagicMock()

                from hello_strands.agent import create_agent

                create_agent()

                mock_model_cls.assert_called_once_with(
                    client_args={
                        "api_key": "test-key",
                        "base_url": "https://test.example.com/v1",
                    },
                    model_id="test-model",
                )


def test_create_agent_passes_system_prompt():
    env = {
        "OPENAI_BASE_URL": "https://test.example.com/v1",
        "OPENAI_API_KEY": "test-key",
        "MODEL_ID": "test-model",
    }
    with patch.dict("os.environ", env):
        with patch("hello_strands.agent.OpenAIModel") as mock_model_cls:
            with patch("hello_strands.agent.Agent") as mock_agent_cls:
                mock_model_cls.return_value = MagicMock()
                mock_agent_cls.return_value = MagicMock()

                from hello_strands.agent import create_agent

                create_agent(system_prompt="Be concise.")

                mock_agent_cls.assert_called_once_with(
                    model=mock_model_cls.return_value,
                    system_prompt="Be concise.",
                )
