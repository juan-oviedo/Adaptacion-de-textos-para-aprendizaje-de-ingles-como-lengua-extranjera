from setuptools import setup, find_packages

setup(
    name="FKGL",
    version="0.1.0",
    description="A short description of your package",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/your_package_name",  # Your repository URL
    packages=find_packages(),
    install_requires=[
        # List dependencies here, e.g., 'numpy', 'pandas>=1.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
