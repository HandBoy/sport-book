def test_on_testing_env(app, mock_env):
    assert app.config["ENV"] == "test"
    assert app.config["SECRET_KEY"] == "test-secret-key"
