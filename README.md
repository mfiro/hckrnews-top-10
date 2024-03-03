# Hacker News Telegram Notifier
Sending top 10 stories of Hacker News to Telegram.
## Motivation
As an avid user of Telegram and a fan of its versatile API, I found it to be an excellent tool for personal projects, especially for delivering notifications directly to my smartphone. This project combines my interest in staying updated with the top stories from Hacker News with the convenience of receiving these updates through Telegram. It serves as a personal notifier.
## Features
* Fetches the top 10 Hacker News stories of the day.
* Sends a formatted message with these stories to a specified Telegram channel.
* Utilizes a Python wrapper for the Hacker News API, **hnconnector**, developed as part of this project.
## Setup
### Prerequisites
* Python 3.x
* A Telegram bot and its API key, obtained from BotFather in Telegram
* A Telegram public channel

### Configuration
* Clone the repository to your local computer.
* There's a **config_sample.py** file provided. Copy this file and rename the copy to **config.py**.
* In config.py, replace the placeholders with your actual Telegram bot API key (bot<APIKEY>) and the target chat ID (e.g., "@myawesomechannel"). The bot must be added as an admin or poster to the target channel.
* Ensure config.py is listed in your .gitignore file to avoid accidentally pushing your credentials to GitHub.

### Running the Project
The best way to run this script is by setting up a cron job on a server, allowing it to run automatically at specified times.
#### Git scraping
While not currently implemented in this project, it's possible to automate the script's execution using GitHub Actions, a method known as "git scraping." For more details, refer to [Simon Willison's blog post]([https://google.com](https://simonwillison.net/2020/Oct/9/git-scraping/)https://simonwillison.net/2020/Oct/9/git-scraping/) on git scraping.

### About hnconnector
This project uses [hnconnector](https://github.com/mfiro/hnconnector), a Python wrapper for the Hacker News API I developed. The library simplifies fetching stories from Hacker News, making it easier to integrate with personal projects like this one.

### Contributing
Contributions to improve the project are welcome. Feel free to fork the repository, make your changes, and submit a pull request.
