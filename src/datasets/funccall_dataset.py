from src.utils.jsonl_utils import read_jsonl_file, save_to_jsonl_file
from src.utils.json_utils import read_json_file, save_to_json_file
from .base_dataset import ToolDataset

import os




class FuncCallDataset(ToolDataset):
    def __init__(self, dataset_name, tool_task, filepath):
        self.dataset_name = dataset_name
        self.tool_task = tool_task
        self.filepath = filepath
        self.datas = self.load_data()

    def load_data(self, ) -> list:
        if self.filepath:
            return self.load_data_from_local(self.filepath)
        elif self.dataset_name and self.tool_task:
            return self.load_data_from_hf(self.tool_task)
        return []

    def load_data_from_local(self, filepath):
        def _load_from_file(filename):
            if "jsonl" in filename:
                return read_jsonl_file(filename)
            elif "json" in filename:
                return read_json_file(filename)

        datas = []
        if os.path.isdir(filepath):
            for filename in os.listdir(filepath):
                datas.extend(_load_from_file(os.path.join(filepath, filename)))
        else:
            datas = _load_from_file(filepath)

        return datas
        
    def load_data_from_hf(self, tool_task):
        pass