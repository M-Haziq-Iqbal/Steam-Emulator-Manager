import appid from "appid";
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function appid(gameName) {
  // Simulating asynchronous behavior with setTimeout
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (gameName === "Dota 2") {
        resolve({ appid: 570 });
      } else {
        reject(new Error("Invalid game name"));
      }
    }, 1000); // Simulating delay
  });
}

rl.question('Enter the game name: ', async (gameName) => {
  try {
    const game = await appid(gameName);
    console.log(`App ID for ${gameName}: ${game.appid}`);
  } catch (error) {
    console.error(error.message);
  } finally {
    rl.close();
  }
});

let dota = await appid("Dota 2");
dota.appid // 570

let mystery = await appid(4000);
mystery.name //  "Garry's Mod"

await appid(/^a/i) // [{"appid":630,"name":"Alien Swarm"},{"appid":635,"name":"Alien Swarm Dedicated Server"},{"appid":640,"name":"Alien Swarm - SDK"},...]