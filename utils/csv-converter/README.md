## CSV Converter

A small script to capture server measurements from a workspace and transform them into CSV.



### How to use it

1. Install project dependencies

```bash
npm install
```

2. Open the `index.js` file, and enter the necessary configuration. Such as _username, password, workspace_. You should also add to the `serverIds` list the ids of the servers you are targeting.

3. Run the script
```bash
npm start
```

4. Once the script has be run, you will find the out inside the `measurements/csv` folder. You will have a file per server.

5. If you need to aggregate all the servers output into one big file. You can run the following command. You will find in the `measurements/csv` folder a new file with the name `aggregated-output.csv`

```bash
npm run merger
```


