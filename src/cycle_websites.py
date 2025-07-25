# -*- coding: utf-8 -*-

import os
import json
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Load the JSON file
with open("data\websites.json", "r") as file:
    data = json.load(file)

# Extract just the URLs into a list
url = [link["url"] for link in data["links"]]

def cycle_websites(urls, duration, display_time):
    """
    Open each URL in a loop using Selenium ChromeDriver for a total duration.

    Args:
        urls (list): List of URLs to visit.
        duration (int): Total time to keep running the loop (in minutes).
        display_time (int): Time to keep each page open (in seconds).
    """

    # Set up Chrome options to suppress logs and go fullscreen
    options = Options()
    options.add_argument("--start-fullscreen")
    options.add_argument("--log-level=3")

    # Initialize the Chrome driver with those options
    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        start_time = time.time()
        duration = duration*60  # converts to minutes

        while (time.time() - start_time) < duration:
            for link in urls:
                if (time.time() - start_time) >= duration:
                    break
                
                # Opens link in fullscreen mode for user
                print(f"Opening: {link}")
                driver.get(link)
                driver.fullscreen_window()
                sleep(display_time)

                # Creates log of visited websites
                export_results(link=link, max_output=100)
    finally:
        driver.quit()

def export_results(link, max_output):
    """
    Create log of visitied websites

    Args:
        link (str): Link appended to logging file
        max_output (int): Max lines in logging file to prevent overloading storage
    """

    # Checks and creates directory of logging file
    os.makedirs("results", exist_ok=True)
    results_dir = os.path.abspath("results")
    log_path = os.path.join(results_dir, "visit_log.txt")

    # Maintains logging file by appending each link opened ...
    #   and clearing out once reaching max output
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            lines = f.readlines()
        if len(lines) >= max_output:
            os.remove(log_path)
    log_path = os.path.join("results", "visit_log.txt")
    with open(log_path, "a") as f:
        f.write(f"{time.ctime()}: Visited {link}\n")


cycle_websites(url=url, duration=5, display_time=5)