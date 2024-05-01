    let playerTurn = 0; 
    var refreshIntervalId;
	var gameStarted = false;
	var gameId = "";
    function main() {
        // Create a button to start the game
        const button = document.createElement('button')
        button.innerText = 'Start Game'
        document.body.appendChild(button);
        button.addEventListener('click', () => {   
            callServer("getPlayerId", "", function(response) {
				playerTurn = response;
                refreshIntervalId = setInterval(function() {
                    checkStartGame(response);
                }, 1000);
            });
        });
    }

	function callServer(actionToDo, valueToPass, callback) {
		$.get("http://127.0.0.1:8000", { action: actionToDo,game_Id:gameId, value: valueToPass, clientId: playerTurn
		}, function (msg_from_server) {
			callback(msg_from_server);
		});
}

function playTurn(tdId) {
	//see if game started or its still time to create the board
	if (!gameStarted){
		moveImage(tdId,gameStarted);
	}else {
		//send the move to the other player
		callServer("isMyTurn","", function(response) {
			if (response == "True") {
				moveImage(tdId,gameStarted);
			}
			else{
				alert("waiting for opponent to play");
			}
		});
	}
}


function startCountdown(duration, display) {
    var timer = duration;
    var countTime = setInterval(function () {
        var minutes = parseInt(timer / 60, 10);
        var seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            clearInterval(countTime);
            display.textContent = "00:00"; // Display 00:00 when the countdown ends
			gameStarted = true;
        }

    }, 1000);
}
function checkStartGame(playerId) {
        callServer("lookingForGame", "", function(response) {
            if (response != "") {
				// if response is not false it means its the gameId
				gameId = response;
				
                console.log("Two players joined. Starting the game...");
                clearInterval(refreshIntervalId);
				// create Board
				createTable(10, 10);
				updateBoard();
				
				//create a new time down
				var clockDiv = document.createElement("div");
				clockDiv.id = "clock";
				clockDiv.style.fontSize = "24px";
				document.body.appendChild(clockDiv);
				var display = document.querySelector('#clock');
				startCountdown(10,display);
	
                setInterval(updateBoard, 1000);
				
            } else {
                console.log("Waiting for another player...");
            }
        });
    }