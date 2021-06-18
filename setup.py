import setuptools
from typing import Dict

# version.py defines the VERSION and VERSION_SHORT variables.
# We use exec here so we don't import snorkel.
VERSION: Dict[str, str]={}
with open("whatsapp_converter/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

with open("README.md", "r") as fh:
    long_description=fh.read()

setuptools.setup(
    name="whatsapp-converter",
    version=VERSION["VERSION"],
    author="Martin Sand",
    author_email="marti.sand.dev@gmail.com",
    description="Use whatsapp-converter to convert your exported WhatsApp chat to a CSV or XLS (Excel spreadsheet) file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandsturm/whatsapp-converter",
    license='LICENSE.txt',
    packages=setuptools.find_packages(),
    install_requires=[
        'tqdm',
        'pyexcel',
        'pyexcel-xlsxw',
        'pyexcel-ods3'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing",
    ],
    python_requires='>=3',
    keywords='whatsapp text converter conversion analysis',
    project_urls={  # Optional
        "Source": "https://github.com/sandsturm/whatsapp-converter/",
        "Bug Reports": "https://github.com/sandsturm/whatsapp-converter/issues",
    },
    entry_points={
        "console_scripts": [
            "whatsapp-converter=whatsapp_converter.__main__:main",
        ]
    },
    test_suite='nose.collector',
    tests_require=['nose'],
)
