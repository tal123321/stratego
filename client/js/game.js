    let playerTurn = 0; 
    var refreshIntervalId;
	var gameStarted = false;
	var gameId = "";
    function main() {
        // Create a button to start the game
        const button = document.createElement('button')
        button.innerText = 'Start Game'
		button.id = "idToRemove";
        document.body.appendChild(button);
        button.addEventListener('click', () => {  
		
            callServer("getPlayerId", "", function(response) {
				playerTurn = response;
				document.getElementById('idToRemove').remove();
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

function handleKeyDown(event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Prevent the default behavior of Enter key in input field
    addText();
  }
}

function addText() {
  var inputTextValue = document.getElementById("input-text").value;
  if (inputTextValue.trim() !== "") {
    document.getElementById("textContainer").textContent += inputTextValue;
    document.getElementById("input-text").value = ""; // Clear the input field after adding text
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
				
				//create a new time down
				var clockDiv = document.createElement("div");
				clockDiv.id = "clock";
				clockDiv.style.fontSize = "24px";
				document.body.appendChild(clockDiv);
				var display = document.querySelector('#clock');
				startCountdown(10,display);
				
				// create the chat and the place to write
				// Create a div element
				var textContainer = document.createElement("div");
				textContainer.setAttribute("id", "textContainer");
				textContainer.setAttribute("style", "border: 1px solid black; padding: 10px; margin-bottom: 10px;");
				document.body.appendChild(textContainer);

				// Create an input element for text input
				var inputText = document.createElement("input");
				inputText.setAttribute("type", "text");
				inputText.setAttribute("id", "input-text");
				inputText.setAttribute("placeholder", "Type your text here...");
				inputText.addEventListener("keydown", handleKeyDown);
				document.body.appendChild(inputText);

				// Create a button for adding text
				var addButton = document.createElement("button");
				addButton.textContent = "Add Text";
				addButton.addEventListener("click", addText);
				document.body.appendChild(addButton);
				// create Board
				createTable(10, 10);
				updateBoard();
                setInterval(updateBoard, 1000);
				
            } else {
                console.log("Waiting for another player...");
            }
        });
    }