
    // Function to be executed onclick 
    var counter = 0; // check if you need to remove the image or add it
    var lastTdId; // the id of the td that we need to remove the image from
    let td; // current td to add the image
    let playerTurn = 0; // decide who plays first
    let startgame = false;
    var refreshIntervalId;

    function moveImage(tdId) {
        td = document.getElementById(tdId);
        
        if (counter % 2 == 1 && !td.className.includes('image')) {
            
            // Check if the location of the new image is legal
            if (!checkIfLocationOk(lastTdId.slice(-2), tdId.slice(-2)))
                return;
            counter++;
            
            // Send the move to the server
            callServer("playTurn", lastTdId.toString() + tdId.toString(), playerTurn, function(response) {
                updateBoard()
            });
        } else if (counter % 2 == 0 && td.className.includes('image')) {
            lastTdId = tdId;
            counter++;
        }
    }

    let lastTd;
    function createBoard(tdId) {
        // If row is smaller than 5 it means the tile is not a card of a player
        if (tdId[0] < 6)
            return;
        
            
        if (counter % 2 == 1) {
            let td = document.getElementById(tdId);
        
            lastTdClass = document.getElementById(lastTdId).className;
            document.getElementById(lastTdId).className = td.className;
            document.getElementById(tdId).className = lastTdClass;
        } else
            lastTdId = tdId;
        counter++;
    }

    function main() {
        // Create the board
        createTable(10, 10);
        // Create a button to start the game
        const button = document.createElement('button')
        button.innerText = 'Start Game'
        document.body.appendChild(button);
        button.addEventListener('click', () => {   
            callServer("getPlayerId", "", "", function(response) {
				playerTurn = response;
                refreshIntervalId = setInterval(function() {
                    checkStartGame(response);
                }, 1000);
            });
        });
    }

    function checkStartGame(playerId) {
        callServer("lookingForGame", "", playerId, function(response) {
            if (response == "True") {
                console.log("Two players joined. Starting the game...");
                clearInterval(refreshIntervalId);
                setInterval(updateBoard, 1000);
				
            } else {
                console.log("Waiting for another player...");
            }
        });
    }

 function createTable(rows, cols) {
    // Create a table element
    var table = document.createElement('table');

    // Create rows and cells
    for (var i = 0; i < rows; i++) {
      var row = document.createElement('tr');

      for (var j = 0; j < cols; j++) {
        var cell = document.createElement('td');
		
		cell.setAttribute('id',(i).toString() + (j).toString());
		
		// decide which class to add to each td 
		cell.classList.add(classToAdd(i+1,j+1));
        if (cell.className!= "green" && cell.className!= "blue") 
			cell.classList.add("board_piece");
        // Add an onclick event to each cell
		
		let rowOfCell = i;
		let colOfCell = j;
		if (cell.classList[0] != "blue"){
		cell.addEventListener('click', function(event) {
			playTurn((rowOfCell).toString() + (colOfCell).toString());
		});
		}
        row.appendChild(cell);
      }

      // Append the row to the table
      table.appendChild(row);
    }

    // Append the table to the body of the document
    document.body.appendChild(table);
  }
  
// check if we want to move the image to a new location which is legal
function checkIfLocationOk(lastTdId,tdId) {
	if( Math.abs(tdId[1]-lastTdId[1])>1)
		return false;
			
	if( Math.abs(tdId[0]-lastTdId[0])>1)
		return false;
	return true;
}

