 function createGame(rows, cols) {
    // Get the container element
    var container = document.createElement('div');
	container.id = 'contain_game';
    container.setAttribute("style", "display: flex; justify-content: space-between;");
	document.getElementById("left_div").appendChild(container);
	
	
    // Create the table-clock section div
    var tableClockSection = document.createElement("div");
    tableClockSection.setAttribute("class", "table-clock-section");
    tableClockSection.setAttribute("style", "display: flex; flex-direction: column; align-items: flex-start;");

    // Create the table using the createTable function
    let table = createTable(rows, cols);

    // Create the clock div
    var clockDiv = document.createElement("div");
    clockDiv.id = "clock";
    clockDiv.setAttribute("style", "font-size: 24px; margin-bottom: 10px;");

    // Append the table and clock div to the table-clock section
    tableClockSection.appendChild(clockDiv);
    tableClockSection.appendChild(table);

    // Create the text section div
    var textSection = document.createElement("div");
    textSection.setAttribute("class", "text-section");
    textSection.setAttribute("style", "flex: 1; margin-left: 20px;");

    // Create the textContainer div
    var textContainer = document.createElement("div");
    textContainer.setAttribute("id", "textContainer");
    textContainer.setAttribute("style", "border: 1px solid black; padding: 10px; margin-bottom: 10px;");

    // Create an input element for text input
    var inputText = document.createElement("input");
    inputText.setAttribute("type", "text");
    inputText.setAttribute("id", "input-text");
    inputText.setAttribute("placeholder", "Type your text here...");

    // Create a button for adding text
    var addButton = document.createElement("button");
    addButton.textContent = "Add Text";
    addButton.addEventListener("click", sendText);

    // Append the textContainer, inputText, and addButton to the text section
    textSection.appendChild(textContainer);
    textSection.appendChild(inputText);
    textSection.appendChild(addButton);

    // Append the text section and table-clock section to the container
    container.appendChild(tableClockSection);
    container.appendChild(textSection);
}
  
function createTable(rows, cols) {
    // Create a table element
    var table = document.createElement('table');

    // Create rows and cells
    for (var i = 0; i < rows; i++) {
        var row = document.createElement('tr');
        for (var j = 0; j < cols; j++) {
            var cell = document.createElement('td');
            cell.setAttribute('id', i.toString() + j.toString());

            // Add dragstart event to each cell
            cell.addEventListener('dragstart', function(event) {
                event.dataTransfer.setData('text/plain', event.target.id);
            });

            // Make the cell draggable
            cell.setAttribute('draggable', 'true');
            row.appendChild(cell);
        }
        table.appendChild(row);
    }

    // Add drop and dragover event listeners to the table
    table.addEventListener('drop', function(event) {
        event.preventDefault();
        var data = event.dataTransfer.getData('text/plain');
        var target = event.target;

        // Ensure the drop target is a table cell
        if (target.tagName.toLowerCase() === 'td') {
            playTurn(data, target.id);
        }
    });

    table.addEventListener('dragover', function(event) {
        event.preventDefault();
    });

    return table;
}

// check if we want to move the image to a new location which is legal
function checkIfLocationOk(lastTdId, tdId) {
    var lastTd = document.getElementById(lastTdId);
    var td = document.getElementById(tdId);
    
    // Calculate the absolute difference between rows and columns
    var rowDiff = Math.abs(tdId[0] - lastTdId[0]);
    var colDiff = Math.abs(tdId[1] - lastTdId[1]);
    
    // If the difference in rows or columns is more than 1
    if (rowDiff > 1 || colDiff > 1) {
        // If the card is not a 2, return false
        if (!lastTd.className.includes("2")) {
            return false;
        } else {
            // If the card is a 2, it can jump more than one tile
            // Check if it's a valid jump (only vertical or horizontal)
            if (rowDiff > 0 && colDiff > 0) {
                return false; // diagonal jump is not allowed
            }
            
            // Check if there are cards between initial and final positions
            if (rowDiff === 0) { // Horizontal jump
                var startCol = Math.min(lastTdId[1], tdId[1]);
                var endCol = Math.max(lastTdId[1], tdId[1]);
                for (var col = startCol + 1; col < endCol; col++) {
                    var card = document.getElementById(lastTdId[0] + col);
                    if (!card.className.includes("green")) {
                        return false; // Invalid jump over non-green or non-blue cards
                    }
                }
            } else if (colDiff === 0) { // Vertical jump
                var startRow = Math.min(lastTdId[0], tdId[0]);
                var endRow = Math.max(lastTdId[0], tdId[0]);
                for (var row = startRow + 1; row < endRow; row++) {
                    var card = document.getElementById(row + lastTdId[1]);
                    if (!card.className.includes("green")) {
                        return false; // Invalid jump over non-green or non-blue cards
                    }
                }
            }
        }
    }
	return true;
}

function moveImage(lastTdId, tdId, gameStarted) {
    var td = document.getElementById(tdId);
	var lastTd = document.getElementById(lastTdId);

    // if game is not started 
    if (!gameStarted&&tdId[0] > 5) {
		// Send the move to the server
        callServer("switchCards", lastTdId.toString() + tdId.toString(), function(response) {
			updateBoard();
        });
        return;
    }

    // if game has started and the cell contains an image
    if (gameStarted && lastTd.classList[1].includes("image")&&!td.classList[1].includes("image")) {
        // Check if the location of the new image is legal
        if (!checkIfLocationOk(lastTdId, tdId))
            return;

        // Send the move to the server
        callServer("playTurn", lastTdId.toString() + tdId.toString(), function(response) {
            updateBoard();
        });
    }
}

function updateBoard(){
	//update the board
	callServer("getGame","", function(response) {
		// board will be an array inside of array until the game is over
		//once over it will be the name of the winner
		response = JSON.parse(response);
		let board = response["board"];
		let chat = response["chat"];
		let time = response["time"];
		
		if (!Array.isArray(board)){
			// if the first one is not an array it means game is over
			gameOver(board);
			return;
		}
		
		for (var i = 0; i < 10; i++) {
			for (var j = 0; j < 10; j++) {
				let td = document.getElementById(i.toString()+j.toString());
				let td_class = board[i][j];
				td.className = '';
				if (td_class!="blue") {
					td.classList.add("board_piece");
				}
				td.classList.add(td_class);
			}
		}
		
		//update the chat
		if (chat != "")
			document.getElementById("textContainer").innerHTML = chat + "<br />";
		
		//update the time
		document.getElementById("clock").innerHTML = time;
		if(time == "0:00"){
			gameStarted = true;
		}
	});
}

//end the game
function gameOver(winner){
	if (userName == winner)
		alert("you won");
	else
		alert("you lost");
	document.getElementById("contain_game").remove();
	clearInterval(updateBoardInterval);
	gameStarted = false;
	main();	
}
