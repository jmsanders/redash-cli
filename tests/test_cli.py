from redash.cli import cli


def test_commands_added_to_cli():
    assert "configure" in cli.commands.keys()
    assert "download" in cli.commands.keys()
    assert "edit" in cli.commands.keys()
    assert "list" in cli.commands.keys()
    assert "new" in cli.commands.keys()
