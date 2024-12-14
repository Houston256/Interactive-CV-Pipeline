from setuptools import setup, find_packages

setup(
    name="interactive-cv-pipeline",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "streamlit >= 1.41.1",
        "streamlit_option_menu",
        "opencv-python-headless",
        "pillow",
        "scikit-image",
        "streamlit-image-comparison",
        "toml",
        "pytest",
        "seaborn",
        "pylint"
    ],
)
