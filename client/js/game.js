	var refreshIntervalId;
	var gameStarted = false;
	var gameId = "";
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

	function callServer(actionToDo, valueToPass, callback) {
		$.get("http://127.0.0.1:8000", { action: actionToDo,game_Id:gameId, value: valueToPass, clientId: userName
		}, function (msg_from_server) {
			callback(msg_from_server);
		});
}

function playTurn(lastTdId,tdId) {
	//see if game started or its still time to create the board
	if (!gameStarted){
		moveImage(lastTdId,tdId,gameStarted);
	}else {
		//send the move to the other player
		callServer("isMyTurn","", function(response) {
			if (response == "True") {
				moveImage(lastTdId,tdId,gameStarted);
			}
			else{
				alert("waiting for opponent to play");
			}
		});
	}
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
				
            } else {
                console.log("Waiting for another player...");
            }
        });
    }