from src.utils.jsonl_utils import read_jsonl_file, save_to_jsonl_file
from src.utils.json_utils import read_json_file, save_to_json_file
from .base_dataset import ToolDataset


class ToolSummaryDataset(ToolDataset):
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
        if "jsonl" in filepath:
            return read_jsonl_file(filepath)
        elif "json" in filepath:
            return read_json_file(filepath)
        return []
        
    def load_data_from_hf(self, tool_task):
        pass