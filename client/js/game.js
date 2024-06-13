	var refreshIntervalId;
	var gameId = "";
	var serverIp = "10.0.0.8";
	
	function sendText() {
		var textToAdd = document.getElementById("input-text").value;
		if (textToAdd.trim() !== "") {
			callServer("sendText", textToAdd, function(response) {
				document.getElementById("input-text").value = ""; // Clear the input field after adding text
			});
		}
	}
    function main() {
        // Create a button to start the game
        const button = document.createElement('button');
        button.innerText = 'Start Game';
		button.id = "idToRemove";
        document.getElementById('left_div').appendChild(button);
        button.addEventListener('click', () => {  
			document.getElementById('idToRemove').remove();
            refreshIntervalId = setInterval(function() {
				checkStartGame();
            }, 1000);
        });
    }

async function callServer(actionToDo, valueToPass, callback) {
    // encrypt message
	let encryptedValue = valueToPass;
	if (actionToDo !== "sendSemetricKey") 
		//encryptedValue = await encryptData(valueToPass, semetricKey);

    // send encrypt message
    $.get("http://127.0.0.1:8000", {
        action: actionToDo,
        game_Id: gameId,
        value: valueToPass,
        clientId: userName
    }, function (msg_from_server) {
        callback(msg_from_server);
    });
}

function playTurn(lastTdId,tdId) {
	callServer("playTurn", lastTdId.toString() + tdId.toString(), function(response) {
		updateBoard();
		if (response == "enemy Turn")
			alert("its not your turn")
    });
}

function validateName(name) {
				let isPasswordOk = "ok";
				if (name.includes(' ')) {
					isPasswordOk = "should not consist spaces";
				}
				if (name.length <= 3) {
					isPasswordOk = "should be higher than 3";
				}
				if (name.length >= 16) {
					isPasswordOk = "should be lower than 16";
				}
				return isPasswordOk;
			}

function sendText() {
	var textToAdd = document.getElementById("input-text").value;
	if (textToAdd.trim() !== "") {
		callServer("sendText", textToAdd, function(response) {
			document.getElementById("input-text").value = ""; // Clear the input field after adding text
		});
	}
}

let updateBoardInterval;
function checkStartGame() {
        callServer("lookingForGame", "", function(response) {
            if (response != "") {
				// if response is not false it means its the gameId
				gameId = response;
				
                console.log("Two players joined. Starting the game...");
				//stop calling checkStartGame
                clearInterval(refreshIntervalId);
				
				//remove the top
				document.getElementById('instructions').remove();
				
				// create Board
				createGame(10, 10);
				updateBoard();
                updateBoardInterval = setInterval(updateBoard, 1000);
				
				// Store username in localStorage
				localStorage.setItem(userName, gameId);
            } else {
                console.log("Waiting for another player...");
            }
        });
    }
	function resign(){
		callServer("resign","", function(response) {
			 // Check if the element with id 'contain_game' exists
			  var gameContainer = document.getElementById("contain_game");
			  if (gameContainer) 
				gameContainer.remove();
			//remove the game from localStorge
			localStorage.removeItem(userName);
			clearInterval(updateBoardInterval);
			main();
		});
	}