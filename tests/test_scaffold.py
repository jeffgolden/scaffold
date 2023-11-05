import pytest
import tempfile
import os
import src.scaffold as scaffold
import json
from typing import Dict, Any

@pytest.fixture
def scaffold_dict() -> Dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield {
            'folders':
            [f'{tmpdirname}/docs',
            f'{tmpdirname}/tests'],
            'files': {
                f'{tmpdirname}/README.md' : [],
                f'{tmpdirname}/.gitignore' : ['.vscode', '__pycache__',],
                f'{tmpdirname}/subdir/file' : ['x']
            }
        }


def test_create_folders(scaffold_dict : Dict[str, Any]):
    scaffold.create_folders(scaffold_dict)
    for folder in scaffold_dict['folders']:
        assert os.path.isdir(folder)
            
def test_create_files(scaffold_dict : Dict[str, Any]):
    scaffold.create_files(scaffold_dict)    
    for file, contents in scaffold_dict['files'].items():
        assert os.path.isfile(file)

def test_read_scaffold_file(mocker, scaffold_dict : Dict[str, Any]):
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(scaffold_dict)))
    test_scaffold = scaffold.read_scaffold_file("scaffold.json")
    
    assert scaffold_dict == test_scaffold
