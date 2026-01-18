import os
import json
import pytest
from src.core.template_manager import TemplateManager
from src.core.schemas import PostScale

@pytest.fixture
def temp_manager(tmp_path):
    """
    Creates a TemplateManager instance using a temporary file for each test case.
    This ensures test isolation.
    """
    test_file = tmp_path / "templates.json"
    return TemplateManager(storage_path=str(test_file))

def test_initial_structure(temp_manager):
    """
    Verifies that the initial JSON is created with next_id=1 
    and contains the default template (ID 0).
    """
    templates = temp_manager.load_all()
    
    # Should load the default template created during initialization
    assert len(templates) == 1
    assert templates[0].id == 0
    assert templates[0].name == "default"
    
    # Verify the raw JSON content for the 'next_id' key
    with open(temp_manager.storage_path, "r") as f:
        data = json.load(f)
        assert data["next_id"] == 1
        assert "templates" in data

def test_auto_increment_id(temp_manager):
    """
    Ensures new templates receive sequential IDs based on the internal counter.
    """
    # Mock data for new styles
    style_1 = {"name": "Modern Dark", "scale_type": PostScale.SQUARE}
    style_2 = {"name": "TikTok Vertical", "scale_type": PostScale.VERTICAL}
    
    # Add first custom template
    t1 = temp_manager.add_template(style_1)
    assert t1.id == 1  # Since initial next_id was 1
    
    # Add second custom template
    t2 = temp_manager.add_template(style_2)
    assert t2.id == 2  # Counter should have incremented
    
    # Check if the next_id in the file is now 3
    with open(temp_manager.storage_path, "r") as f:
        data = json.load(f)
        assert data["next_id"] == 3
        assert len(data["templates"]) == 3 # default(0) + t1(1) + t2(2)

def test_delete_persistence_of_counter(temp_manager):
    """
    Verifies that deleting a template does not reset or reuse IDs.
    This prevents conflicts with file names or UI caches.
    """
    # Add a template that will be removed (ID 1)
    temp_manager.add_template({"name": "Temp Style"})
    temp_manager.delete_template(1)
    
    # Add a new one after deletion
    t_new = temp_manager.add_template({"name": "Fresh Style"})
    
    # Even though ID 1 is gone, the new ID must be 2
    assert t_new.id == 2
    
    # Final check on list integrity
    templates = temp_manager.load_all()
    ids = [t.id for t in templates]
    assert 1 not in ids
    assert 2 in ids

def test_data_persistence_between_instances(tmp_path):
    """
    Ensures that data is correctly persisted to disk and can be 
    recovered by a completely new instance of the manager.
    """
    path = str(tmp_path / "persistence_check.json")
    
    # Instance 1: Create and save
    mgr1 = TemplateManager(path)
    mgr1.add_template({"name": "Permanent Style", "font_size": 60})
    
    # Instance 2: Load from the same path
    mgr2 = TemplateManager(path)
    all_templates = mgr2.load_all()
    
    assert len(all_templates) == 2
    assert all_templates[1].name == "Permanent Style"
    assert all_templates[1].font_size == 60
