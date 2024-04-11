# Rates Analysis Automation

## Objective

The purpose of this repository is to automate the rates analysis process for individual plans in rate analysis. It focuses on consolidating related files from providers, establishing tidy DataFrames for these files, and merging them where necessary. This automation facilitates the use of these consolidated data in dashboards and further analysis, streamlining what would otherwise be a manual and time-intensive process.

## Features

- **File Consolidation**: Automates the collection and consolidation of rate analysis files.
- **Data Cleaning and Preparation**: Transforms files into tidy pandas DataFrames, ready for analysis.
- **Data Merging**: Combines related data for comprehensive analysis.
- **Dashboard and Analysis Readiness**: Prepares data in a format that's easily consumed by dashboards and analytical tools.

## How to Use

This repository contains Python scripts designed for specific parts of the rates analysis process. Below is a brief overview of the primary functions:

### `Rates File Puller`

- **Purpose**: To consolidate files based on specific types related to rate analysis.
- **Parameters**:
  - `type`: The type of analysis or file to process (e.g., 'Rates Table Template', 'Network Table Template').
  - `source_folder`: The directory where source files are located.
  - `target_folder`: The destination directory for processed files.

### `Tidy Table Creation`

- **Purpose**: Creates a DataFrame from rate table files, tailored for further analysis.
- **Parameters**:
  - `folder`: The directory containing rate table files.
- **Compatible Templates**
  - `URRT`
  - `Network Template`
  - `Rates Table Template`
  - `Plans & Benefits Template`

## Dependencies

- Python 3.x
- pandas
- os, shutil, re, glob, pathlib (standard library modules)

## Setup and Installation

Ensure you have Python installed on your system. Clone this repository to your local machine:

```bash
git clone [git@github.com:yourusername/yourrepository.git](https://github.com/Marc-Torchio/Rates_Analysis.git)](https://github.com/Marc-Torchio/Rates_Analysis.git)