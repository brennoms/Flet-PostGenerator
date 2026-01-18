# 📸 PostGenerator

**PostGenerator** is a professional tool designed for content creators to transform long-form text into high-quality, sequential visual posts for social media. By leveraging **Python (Pillow)** for precise rendering and **Flet** for a modern mobile experience, it automates the tedious parts of content creation.

## ✨ Key Features

* **📂 Directory Management:** Organize your content by selecting specific project folders for a seamless workflow.
* **🖼️ Interactive Feed Viewer:** Preview your generated posts in a gallery-style layout before exporting.
* **🎨 Customizable Template System:** * **Create & Reuse:** Build visual presets with custom background colors, text styles, and branding.
* **Live Adaptation:** Switch between different templates instantly to see which style fits your current message best.


* **✍️ Template-Based Auto-Generator:**
* **Smart Segmentation:** Automatically splits long-form text into multiple sequential slides based on your template's constraints.
* **Dynamic Layouts:** Custom text alignment and smart vertical centering for perfect visual balance.
* **Typography Control:** Set default fonts and sizes to ensure brand consistency across all posts.



## 🛠️ Tech Stack

* **[Python](https://www.python.org/):** Core engine.
* **[Flet](https://flet.dev/):** Flutter-based UI framework for Python.
* **[Pillow (PIL)](https://www.google.com/search?q=https://python-pillow.org/):** High-precision image processing and rendering.
* **[Textwrap](https://docs.python.org/3/library/textwrap.html):** Intelligent text segmentation logic.

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.9 or higher installed.

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/post-generator-ai.git
cd post-generator-ai

```


2. **Install dependencies:**
```bash
pip install flet Pillow

```


3. **Run the application:**
```bash
flet run main.py

```



## 📱 Building the APK (Android)

To package the project as an installable Android app:

```bash
flet build apk --permissions READ_EXTERNAL_STORAGE WRITE_EXTERNAL_STORAGE

```

## 📋 Roadmap

* [ ] Support for custom fonts (.ttf) via file picker.
* [ ] Dark Mode / Light Mode toggle for the UI.
* [ ] AI-powered caption and hook suggestions.
* [ ] Export directly to social media API.

## 📄 License

Licensed under the **Apache License, Version 2.0** (the "License"). You may not use this project except in compliance with the License. You may obtain a copy of the License at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
