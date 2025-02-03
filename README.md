# Telegram Channel Analysis Project

This project uses the [Telethon](https://docs.telethon.dev/) library to collect and analyze members of a Telegram channel. It identifies potential fake followers based on a simple heuristic and visualizes the distribution of profile photos among collected members.

## Features

- **Data Collection:** Retrieves all members from a specified Telegram channel.
- **Data Analysis:** Separates members by the presence or absence of a profile photo.
- **Fake Follower Identification:** 
  - No profile photo.
  - No username.
  - First name shorter than 3 characters.
- **Visualization:** Displays a pie chart showing the distribution of profile photo usage.

## Prerequisites

Ensure you have the following installed:
- Python 3.x
- Python libraries:
  - [Telethon](https://pypi.org/project/Telethon/)
  - [Matplotlib](https://pypi.org/project/matplotlib/)

## Installation

Install the required libraries using pip:

```bash
pip install telethon matplotlib
