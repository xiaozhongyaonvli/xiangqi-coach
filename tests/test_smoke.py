def test_package_import():
    import xiangqi_core

    assert hasattr(xiangqi_core, "__all__")
