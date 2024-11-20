# Interactive Visualization: CIA World Factbook Data

This repository contains a project focused on **interactive data visualization** using the CIA World Factbook dataset. The goal is to provide dynamic, visually appealing ways to explore global data attributes like GDP, military expenditures, life expectancy, and more, using Python, Matplotlib, and PyQt6.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Data](#data)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Tasks and APIs](#tasks-and-apis)

---

## Introduction

The CIA World Factbook dataset contains key statistics for countries worldwide, covering areas like economy, population, and health. This project creates interactive visualizations to explore and analyze this data. Users can dynamically select attributes for visualization, perform linked brushing, and view detailed country information on demand.

---

## Features

- **Dynamic Bubble Chart**: Scatter plot with customizable size, color, and axes attributes.
- **Interactive Widgets**: Drop-down menus and sliders for runtime attribute selection.
- **Linked Brushing**: Synchronize data selection between two visualizations.
- **Details on Demand**: Hover over data points to view country-specific attributes.

---

## Data

The dataset includes attributes for various countries, such as:

- **GDP per Capita**
- **Military Expenditures**
- **Population**
- **Life Expectancy**
- **Birth Rate**
- **Energy Consumption**
- **National Debt**

---

## Prerequisites

Python 3.11 or higher

Required Libraries:
- `pandas` - 2.2.2
- `matplotlib` - 3.9.2
- `pyqt6` - 6.5.1
- `argparse` - 1.1

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/CIA-World-Factbook-Visualization.git
   cd CIA-World-Factbook-Visualization
