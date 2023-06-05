# Web Data Scraping

This project focuses on web data scraping and extraction. The code provided utilizes Python and various libraries to scrape data from a specified URL, parse the HTML content, and extract relevant information.

## Project Description

The "Web Data Scraping" project provides a graphical user interface (GUI) developed using PyQt5, allowing users to input a URL and initiate the scraping process. The application performs the following key functionalities:

- Retrieves the HTML content of the specified URL using the requests library.
- Parses the HTML content using the BeautifulSoup library to extract desired data.
- Displays the extracted data in a table format within the GUI using the QtWidgets.QTableWidget widget.
- Supports pausing and resuming the scraping process using threading and events.

## Getting Started

To run the project, follow these steps:

1. Install the necessary dependencies: `requests`, `beautifulsoup4`, `PyQt5`.
2. Clone or download the project source code.
3. Open the terminal or command prompt and navigate to the project directory.
4. Execute the following command to start the application:

python main.py

## Usage
1. Launch the application.
2. Enter the URL of the web page to be scraped in the provided input field.
3. Click the "Start" button to initiate the scraping process.
4. The application will retrieve the HTML content, extract relevant information, and display it in the table.
5. Click the "Pause" button to temporarily pause the scraping process.
6. To resume the scraping, click the "Resume" button.

## Dependencies
The project relies on the following dependencies:

- requests: Used for making HTTP requests to retrieve web page content.
- beautifulsoup4: Used for parsing HTML content and extracting relevant data.
- PyQt5: Used for developing the graphical user interface.
Make sure to install these dependencies before running the project.

## Results

![image](https://github.com/TanNguyen0108/Data-Project/assets/109364182/bf0a923b-34f7-4fd3-a5bd-32fc70b80e41)


## Contributions
Contributions to the project are welcome. If you encounter any issues or have suggestions for improvements, please create a new issue or submit a pull request.
