# Kick.com Account generator
Kick Account generator

⭐️
## Features
- Fully based on Requests
- Threads support
- Proxy Support
- Follow channels on each account created (requires proxies)
- Email-Based Account Creation: With <a href="https://github.com/Bluyx/email-api">email api</a> You can Generate accounts using email addresses from your custom domain and receive the verification code automatically. (Use it like this: xxx@example.com) OR you can use <a href="https://kopeechka.store/?ref=28978">Kopeechka.store</a>
- Saving Generated Accounts: Saving all generated account details in a JSON/TXT file.
- Realistic usernames
- Customizable Options: Choose between realistic, random or specific usernames for each account and Choose whether to use random or specific passwords.

🔴 You might still get the 'The browser is not supported.' error

🔴 Following channels after each account is created might not work
## Requirements
- Emails using <a href="https://kopeechka.store/?ref=28978">Kopeechka.store</a> or <a href="https://github.com/Bluyx/email-api">email api</a>
- <a href="https://salamoonder.com/">Salamoonder api key (Kasada Solver)</a>
- proxies

## Installation
```bash
git clone https://github.com/Bluyx/Kick.com-account-generator
cd Kick.com-account-generator
pip install -r requirements.txt
```
Rename config.json.example to config.json<br>
Edit the `config.json` file<br>
If you want to use <a href="https://kopeechka.store/?ref=28978">Kopeechka.store</a> then put your token and the mail you want<br>
If you want to use <a href="https://github.com/Bluyx/email-api">Custom domain</a> then put your API URL, imap, emails domain 
```bash
python main.py
```
## Configuration
`config.json`
- `kopeechka`: This section is used when you want to use [Kopeechka.store](https://kopeechka.store/?ref=28978) for email-based account creation.
    - `kopeechkaToken`: Your Kopeechka.store token.
    - `domains`: The email domains you want to use for account creation.

- `salamoonder_apiKey`: Your [Salamoonder API key](https://salamoonder.com/), used for solving Kasada challenges.

- `apiURL`: The URL of your custom email API, used when you want to use a custom domain for email-based account creation.

- `imap`: The IMAP server of your custom email domain.

- `domain`: The domain of your custom email addresses.

- `settings`: Various settings for the account generator.
    - `follow`: An array of usernames that each generated account will follow.
    - `saveAs`: The format to save generated accounts in (1 for JSON with cookies, 2 for JSON without cookies, 3 for TXT).
    - `proxiesFile`: The path to a file containing proxies to use.
    - `AccountsCount`: The number of accounts to generate.
    - `usernamesType`: The type of usernames to generate (1 for realistic, 2 for random, 3 for specific (adding numbers to the end)).
    - `passwordsType`: The type of passwords to use (1 for random, 2 for specific).
    - `password`: The specific password to use for all accounts (only used when `passwordsType` is 2).
    - `emailsType`: The type of emails to use (1 for Kopeechka.store, 2 for custom domain).
    - `threads`: The number of threads to use for account generation.
## Screenshots
![App Screenshot](https://cdn.discordapp.com/attachments/1192914223232188486/1220084042955882577/ss.png?ex=660da6cf&is=65fb31cf&hm=a86c0ca0677c375c6446311a282be6c5065a286cd32b0f93af023e6d6365e525&)


## Todo List
- Better UI
- Make it follow channels of the user's choice after each account is created
- Handle more errors

## Contant
- Discord: <a href="https://discord.com/users/251794521908576257">2yv</a>
