def test_true():
    assert True

def test_env_imports():
    import numpy, pandas, sklearn  # imports must succeed

def test_configs_load():
    import yaml
    open("params.yaml").close()
    open("config/config.yaml").close()

