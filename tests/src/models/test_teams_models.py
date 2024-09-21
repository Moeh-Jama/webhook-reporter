from src.models.teams_model import Column, ColumnSet, TextBlock


def test_text_block():
    text_block = TextBlock(text="Hello, world!", wrap=True, size="medium", weight="bold", spacing=None)
    expected = {
        "type": "TextBlock",
        "text": "Hello, world!",
        "wrap": True,
        "size": "medium",
        "weight": "bold"
    }
    assert text_block.to_dict() == expected

def test_column():
    column = Column(
        width="auto",
        items=[
            TextBlock(text="Item 1", wrap=False, size=None, weight=None, spacing=None),
            TextBlock(text="Item 2", wrap=True, size="small", weight=None, spacing="large")
        ]
    )
    expected = {
        "type": "Column",
        "width": "auto",
        "items": [
            {"type": "TextBlock", "text": "Item 1", "wrap": False},
            {"type": "TextBlock", "text": "Item 2", "wrap": True, "size": "small", "spacing": "large"}
        ]
    }
    assert column.to_dict() == expected

def test_column_set():
    column_set = ColumnSet(
        
        columns=[
            Column(
                width="auto",
                items=[
                    TextBlock(text="Column 1, Item 1", wrap=True, size=None, weight=None, spacing=None),
                    TextBlock(text="Column 1, Item 2", wrap=False, size="medium", weight="bold", spacing=None)
                ]
            ),
            Column(
                width="stretch",
                items=[
                    TextBlock(text="Column 2, Item 1", wrap=True, size=None, weight=None, spacing="small"),
                    TextBlock(text="Column 2, Item 2", wrap=True, size="large", weight=None, spacing=None)
                ]
            ),
            Column(
                items=[
                    TextBlock(text="Column 3, Item 1", wrap=True, size=None, weight=None, spacing="small"),
                    TextBlock(text="Column 3, Item 2", wrap=True, size="large", weight=None, spacing=None)
                ]
            )
        ]
    )
    expected = {
        "type": "ColumnSet",
        "columns": [
            {
                "type": "Column",
                "width": "auto",
                "items": [
                    {"type": "TextBlock", "text": "Column 1, Item 1", "wrap": True},
                    {"type": "TextBlock", "text": "Column 1, Item 2", "wrap": False, "size": "medium", "weight": "bold"}
                ]
            },
            {
                "type": "Column",
                "width": "stretch",
                "items": [
                    {"type": "TextBlock", "text": "Column 2, Item 1", "wrap": True, "spacing": "small"},
                    {"type": "TextBlock", "text": "Column 2, Item 2", "wrap": True, "size": "large"}
                ]
            },
            {
                "type": "Column",
                "items": [
                    {"type": "TextBlock", "text": "Column 3, Item 1", "wrap": True, "spacing": "small"},
                    {"type": "TextBlock", "text": "Column 3, Item 2", "wrap": True, "size": "large"}
                ]
            }
        ]
    }
    assert column_set.to_dict() == expected