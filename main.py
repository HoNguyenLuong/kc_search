import pandas as pd
import requests
from tqdm import tqdm
from file_handler import write_to_json
from mylog import logging
from typing import List, Dict

datasets = ['vlsp2016', 'vlsp2018', 'vlsp2021']
filenames = ['dev', 'test', 'train']

URL_SEARCH = "http://localhost:9920/search"
CHECKPOINT_FILE = "checkpoint.txt"
DISTANCE_THRESHOLD = 40

def search_url(url: str, k: int) -> List[Dict]:
    """Search for a URL with a limit of results."""
    payload = {"url": url, "k": k}
    try:
        response = requests.post(URL_SEARCH, json=payload)
        response.raise_for_status()
        logging.info(f"Search successful for {url}. Results: {response.json()}")
        
        # Truy cập vào danh sách 'results' bên trong phản hồi
        results = response.json().get("results", [])
        
        # Lọc kết quả dựa trên ngưỡng distance và kiểm tra loại dữ liệu
        filtered_results = [
            result for result in results
            if isinstance(result, dict) and result.get("distance", float("inf")) <= DISTANCE_THRESHOLD
        ]
        
        return filtered_results
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to search {url}: {str(e)}")
        return []



def get_url_from_id(urls: List[str], k: int = 10) -> Dict[str, List[str]]:
    """Get top URLs from a list of input URLs by searching."""
    results_dict = {}
    for url in urls:
        results_dict[url] = search_url(url, k)
    return results_dict

def read_checkpoint() -> int:
    """Đọc chỉ số cuối cùng đã xử lý từ file checkpoint."""
    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0  # Nếu không có checkpoint, bắt đầu từ 0

def update_checkpoint(last_index: int):
    """Cập nhật checkpoint với chỉ số mới nhất."""
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(last_index))
        
if __name__ == '__main__':
    checkpoint = read_checkpoint()  # Đọc checkpoint hiện tại
    
    for dataset in datasets:
        for filename in filenames:
            current_file = f'{dataset}/{filename}.csv'
            file_path = current_file
            
            # Đọc file CSV và lấy cột 'id' và 'url'
            df = pd.read_csv(file_path)
            imgid_url_list = df[['id', 'url']].rename(columns={'id': 'imgid'}).to_dict(orient='records')
            
            # Danh sách lưu kết quả tìm kiếm
            list_documents = []
            
            # Tìm kiếm và lưu kết quả vào list_documents, bắt đầu từ checkpoint
            for index, entry in enumerate(tqdm(imgid_url_list[checkpoint:], desc=f"Processing {file_path}")):
                actual_index = checkpoint + index  # Tính chỉ số thực tế
                
                imgid = entry['imgid']
                url = entry['url']
                
                # Gọi hàm tìm kiếm và lưu kết quả
                search_results = get_url_from_id([url], k=10)
                list_documents.append({'imgid': imgid, 'url': url, 'search_results': search_results.get(url, [])})
                
                # Cập nhật checkpoint sau mỗi mục xử lý
                update_checkpoint(actual_index)

            
            # Ghi kết quả vào file JSON sau khi hoàn thành file hiện tại
            
            path_to_file_json = f'{current_file}.json'
            write_to_json(path_to_file_json, list_documents)
            
            # Reset checkpoint khi hoàn thành file
            checkpoint = 0
            update_checkpoint(checkpoint)
