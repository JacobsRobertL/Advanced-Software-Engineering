from unittest.mock import patch, MagicMock


def test_view_song_tags_retrieves_tags():
    from ui.app_window import AppWindow

    app = MagicMock()

    app.track_results_listbox.curselection.return_value = (0,)
    app.track_search_results = [
        {
            "type": "track",
            "artist": "aespa",
            "title": "Drama"
        }
    ]

    mock_response = {
        "toptags": {
            "tag": [
                {"name": "k-pop"},
                {"name": "dance"},
                {"name": "electropop"}
            ]
        }
    }

    with patch("ui.app_window.get_song_tags", return_value=mock_response) as mock_get_tags, \
         patch("ui.app_window.tk.Toplevel"), \
         patch("ui.app_window.ttk.Label"), \
         patch("ui.app_window.ttk.Button"):

        AppWindow._on_view_song_tags(app)

    mock_get_tags.assert_called_once_with("aespa", "Drama")