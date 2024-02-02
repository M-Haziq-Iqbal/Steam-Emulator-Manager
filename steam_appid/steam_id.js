// Importing the required package
const appid = require("appid");

// Get the game name from command-line arguments
const gameId = Number(process.argv[2]); // The first argument after 'node' and the script name

// Define an asynchronous function to use await
async function getGameName() {
   try {
      // Calling the appid function asynchronously
      const gameName = await appid(gameId); // Returns { appid: 10, name: "Counter-Strike" }
      process.stdout.write(gameName.name);
      // console.log(`Game info: ${JSON.stringify(gameName)}`);
   } catch (error) {
      console.error('Error:', error);
   }
}

// Call the asynchronous function to start execution
getGameName();