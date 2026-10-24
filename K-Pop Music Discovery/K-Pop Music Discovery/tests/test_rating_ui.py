from unittest.mock import MagicMock
from ui.app_window import AppWindow


def test_selecting_song_loads_rating():
    app = MagicMock()
    app.discovery_listbox.curselection.return_value = (0,)
    app.discovery_results = [{"title": "WOKE UP", "artist": "XG"}]
    app.db_repo.get_song_rating.return_value = 4

    AppWindow._on_discovery_selected(app, None)

    app.db_repo.get_song_rating.assert_called_once_with("WOKE UP", "XG")
    app.rating_var.set.assert_called_once_with("4")


def test_saving_selected_song_rating():
    app = MagicMock()
    app.discovery_listbox.curselection.return_value = (0,)
    app.discovery_results = [{"title": "WOKE UP", "artist": "XG"}]
    app.rating_var.get.return_value = "5"

    from unittest.mock import patch

    with patch("ui.app_window.messagebox.showinfo"):
        AppWindow._on_save_rating(app)

    app.db_repo.save_rating.assert_called_once_with("WOKE UP", "XG", 5)