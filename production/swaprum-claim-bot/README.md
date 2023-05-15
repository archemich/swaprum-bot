# swaprum-claim-bot

## Usage
Install `swaprum-claim-bot` package.
```shell
pip3 install .
```

Run the bot.
```shell
swaprum-claim-bot --csv-wallets /path/to/csv/wallets.csv
```

### .csv file requirements
CSV file must contain at least two columns where the second column is a wallet address.
Also csv must have `;` delimter and `;;;` endline string.
