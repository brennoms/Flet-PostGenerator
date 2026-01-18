import os
import shutil
from PIL import Image
from src.core.saver import PostSaver

def test_save_single_image(tmp_path):
    img = Image.new("RGB", (10, 10), color="red")
    base_dir = str(tmp_path)
    
    path = PostSaver.save_post([img], base_dir, "Single Post")
    
    assert os.path.isfile(path)
    assert path.endswith("single-post.png")

def test_save_carousel_folder(tmp_path):
    img1 = Image.new("RGB", (10, 10), color="red")
    img2 = Image.new("RGB", (10, 10), color="blue")
    base_dir = str(tmp_path)
    
    path = PostSaver.save_post([img1, img2], base_dir, "My Carousel")
    
    assert os.path.isdir(path)
    assert os.path.isfile(os.path.join(path, "1.png"))
    assert os.path.isfile(os.path.join(path, "2.png"))