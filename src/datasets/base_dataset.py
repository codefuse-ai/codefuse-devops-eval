from src.utils.jsonl_utils import read_jsonl_file, save_to_jsonl_file
from src.utils.json_utils import read_json_file, save_to_json_file



class ToolDataset:
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
        ''''''
        pass
        
    def load_data_from_hf(self, tool_task):
        pass
        
    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.datas):
            current_item = self.datas[self.current_index]
            self.current_index += 1
            return current_item
        else:
            raise StopIteration

    def __len__(self):
        return len(self.datas)
