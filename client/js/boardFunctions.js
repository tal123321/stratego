var counter = 0; // check if you need to remove the image or add it
var lastTdId; // the id of the td that we need to remove the image from
let td; // current td to add the image
	
 function createGame(rows, cols) {
    // Create a table element
	var container = document.getElementById("contain_board");
    var table = document.createElement('table');

    // Create rows and cells
    for (var i = 0; i < rows; i++) {
      var row = document.createElement('tr');

      for (var j = 0; j < cols; j++) {
        var cell = document.createElement('td');
		
		cell.setAttribute('id',(i).toString() + (j).toString());
        // Add an onclick event to each cell
		
		 // Add an event listener for dragstart to each cell
        cell.addEventListener('dragstart', function(event) {
            // Set the data to be transferred to the ID of the cell
            event.dataTransfer.setData('text/plain', event.target.id);
        });

        // Add the draggable attribute to the cell
        cell.setAttribute('draggable', 'true');

        row.appendChild(cell);
      }

      // Append the row to the table
      table.appendChild(row);
    }
	
	
	
	// Add event listener for the drop event on the table
	table.addEventListener('drop', function(event) {
		event.preventDefault();
		var data = event.dataTransfer.getData('text/plain'); // Get the data from the drag operation
		var target = event.target; // Get the drop target

		// Check if the drop target is a table cell
		if (target.tagName.toLowerCase() === 'td') {
			// Call playTurn function with appropriate parameters
			playTurn(data,target.id);
		}
	});

	// Add event listener for the dragover event on the table
	table.addEventListener('dragover', function(event) {
		event.preventDefault();
	});

    // Append the table to the body of the document
	// create the chat and the place to write
	// Create a div element
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
	//create a new time down
	var clockDiv = document.createElement("div");
	clockDiv.id = "clock";
	clockDiv.style.fontSize = "24px";
	
	
    // Append the table to the container
	container.appendChild(table);

	// Append the textContainer, inputText, and addButton to the container
	container.appendChild(clockDiv);
	container.appendChild(textContainer);
	container.appendChild(inputText);
	container.appendChild(addButton);
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
            if (rowDiff > 1 && colDiff > 1) {
                return false; // diagonal jump is not allowed
            }
            
            // Check if there are cards between initial and final positions
            if (rowDiff === 0) { // Horizontal jump
                var startCol = Math.min(lastTdId[1], tdId[1]);
                var endCol = Math.max(lastTdId[1], tdId[1]);
                for (var col = startCol + 1; col < endCol; col++) {
                    var card = document.getElementById(lastTdId[0] + col);
                    if (!card.className.includes("green") && !card.className.includes("blue")) {
                        return false; // Invalid jump over non-green or non-blue cards
                    }
                }
            } else if (colDiff === 0) { // Vertical jump
                var startRow = Math.min(lastTdId[0], tdId[0]);
                var endRow = Math.max(lastTdId[0], tdId[0]);
                for (var row = startRow + 1; row < endRow; row++) {
                    var card = document.getElementById(row + lastTdId[1]);
                    if (!card.className.includes("green") && !card.className.includes("blue")) {
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

    // if game is not started 
    if (!gameStarted) {
        if (tdId[0] > 5) {
            // Send the move to the server
            callServer("switchCards", lastTdId.toString() + tdId.toString(), function(response) {
                updateBoard();
            });
            return;
        }
    }

    // if game has started and the cell contains an image
    if (gameStarted && !td.classList.contains("image")) {
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
	callServer("getBoard","", function(response) {
		if (response == "" || response === undefined)
			return;
		else if (!response.includes(" ")){
			// if it doesn't include space it means the game is over
			gameOver(response);
			return;
		}
		let boardArray = response.split(" ")
		let counter = 0
		
		for (var i = 0; i < 10; i++) {
			for (var j = 0; j < 10; j++) {
				let td = document.getElementById(i.toString()+j.toString());
				let td_class = boardArray[counter];
				td.className = '';
				if (td_class!="blue") {
					td.classList.add("board_piece");
				}
				td.classList.add(td_class);
				counter++;
			}
		}
	});
	//update the chat
	callServer("getText","", function(response) {
		if (response != "")
			document.getElementById("textContainer").innerHTML = response + "<br />";
	});
	
	//
	//update the time
	callServer("getTime","", function(response) {
		document.getElementById("clock").innerHTML = response;
		if(response == "0:00"){
			gameStarted = true;
		}
	});
}	

//end the game
function gameOver(winner){
	if (playerTurn == winner)
		alert("you won");
	else
		alert("you lost");
	document.getElementById("contain_board").remove();
	clearInterval(updateBoardInterval);
	main();	
}
