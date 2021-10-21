const { Parser } = require("json2csv");
const axios = require("axios");
const fs = require("fs");
const argv = require("minimist")(process.argv.slice(2));

///////////////////////////////////////////////////////////
//////////////// Configuration ////////////////////////////
///////////////////////////////////////////////////////////

// 1. Add credentials
const username = "";
const password = "";
const workspace = "";

// 2. Add server IDs
const serverIds = [];

///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
////////////////// DON't CHANGE ///////////////////////////
///////////////////////////////////////////////////////////

/**
 * Help command
 */
if (argv.help || argv.h) {
  console.log("\nGetting started.\n");
  console.log(
    "1. Open the index.js file. Add your username and password to authenticate your request"
  );
  console.log("2. Populate the serverIds list");
  console.log(
    "3. If you would like to save a copy of the API JSON response, pass the flag --verbose\n"
  );
  console.log(
    "Check the measurements folder, you will find two sub-folders in it. \nJSON will contained the json server response if you passed the --verbose flag. \nCSV will have the output in csv files containing the measurements of a server. You will have as many csv files as server IDS"
  );
  return;
}

const serversNotFound = [];
let token = "";

const aggregateJSON = [];

// authenticate
const authenticate = async () => {
  const data = JSON.stringify({
    username,
    password,
  });

  const config = {
    method: "POST",
    url: `https://${workspace}.tidalmg.com/api/v1/authenticate?`,
    headers: {
      "Content-Type": "application/json",
    },
    data: data,
  };

  try {
    const response = await axios(config);

    if (response.data.failure) {
      throw ":(";
    }
    token = response.data.access_token;
  } catch (error) {
    throw "Unable to authenticate :(";
  }
};

authenticate()
  .then(() => {
    console.log("Processing .....");
    return Promise.all(
      serverIds.map(async (server) => {
        let responseAPI;
        try {
          // get measurements from MMP
          responseAPI = await axios({
            method: "GET",
            url: `https://${workspace}.tidalmg.com/api/v1/servers/${server}/measurements?filters[field_name]=~_timeseries`,
            headers: {
              Authorization: token,
            },
          });
        } catch (error) {
          if (argv.verbose) {
            console.log(error.response.data.errors[0]);
          }
          serversNotFound.push(server);
          return;
        }

        if (argv.withJSON) {
          try {
            const serverData = JSON.stringify(responseAPI.data, null, 2);

            fs.writeFile(
              `output/json/server-${server}.json`,
              serverData,
              (err) => {
                if (err) throw err;
              }
            );
          } catch (error) {
            if (argv.verbose) {
              console.log(error);
            }
            console.log("something is wrong with saving API server response");
          }
        }

        // csv conversion
        const fields = [
          "id",
          "measurable_id",
          "measurable_type",
          "field_name",
          "name",
          "value",
          "timestamp",
          "created_at",
          "updated_at",
        ];

        const csv = new Parser({ fields });

        return fs.writeFile(
          `output/csv/server-${server}-output.csv`,
          csv.parse(responseAPI.data),
          function (err) {
            if (err) {
              if (argv.verbose) {
                console.error(err);
              }
              throw err;
            }
          }
        );
      })
    );
  })
  .then(() => {
    console.log("Process completed!");
    console.log("The following servers had problems", serversNotFound);
  })
  .catch((e) => {
    console.log("Error => ", e);
  });
