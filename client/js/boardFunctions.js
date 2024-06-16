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

    // Create the clock divs
	var Player1clock = document.createElement("div");
	Player1clock.id = "clock1";
	Player1clock.setAttribute("style", "font-size: 24px; margin-bottom: 10px;");

	var Player2clock = document.createElement("div");
	Player2clock.id = "clock2";
	Player2clock.setAttribute("style", "font-size: 24px; margin-bottom: 10px;");

	// Create two <div> elements to display the ratings and clocks
	let p1 = document.createElement('div');
	p1.setAttribute("style", "display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;");

	let p2 = document.createElement('div');
	p2.setAttribute("style", "display: flex; justify-content: space-between; align-items: center;");

	// Create spans to hold the ratings
	let rating1 = document.createElement('span');
	let rating2 = document.createElement('span');

	// Get the names and the rating
	callServer("getRating", "", function(response) {
		response = response.split(' ');
		rating1.textContent = response[0];
		rating2.textContent = response[1];
	});

	// Append the ratings and clocks to the <div> elements
	p1.appendChild(rating1);
	p1.appendChild(Player1clock);

	p2.appendChild(rating2);
	p2.appendChild(Player2clock);

	// Append the <div> elements and table to the table-clock section
	tableClockSection.appendChild(p1);
	tableClockSection.appendChild(table);
	tableClockSection.appendChild(p2);
	
	//create button to startGame
    var startGameBottom = document.createElement("button");
	startGameBottom.id = "startGame";
    startGameBottom.textContent = "ready to start Game?";
    startGameBottom.addEventListener("click", readyStartGame);
	tableClockSection.appendChild(startGameBottom);
	
	//create button resign
    var resignBottom = document.createElement("button");
    resignBottom.textContent = "resign";
    resignBottom.addEventListener("click", resign);
	tableClockSection.appendChild(resignBottom);
	
    // Create the text section div
    var textSection = document.createElement("div");
    textSection.setAttribute("class", "text-section");
    textSection.setAttribute("style", "flex: 1; margin-left: 20px;");

    // Create the textContainer div
    var textContainer = document.createElement("div");
    textContainer.setAttribute("id", "textContainer");
    textContainer.setAttribute("style", "border: 1px solid black; padding: 10px; margin-bottom: 10px; width: 1000; height: 100px; overflow-y: auto;");

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

function updateBoard(){
	//update the board
	callServer("getGame","", function(response) {
		// board will be an array inside of array until the game is over
		//once over it will be the name of the winner
		response = JSON.parse(response);
		let board = response["board"];
		let chat = response["chat"];
		let timeFirstPlayer = response["time1"];
		let timeSecondPlayer = response["time2"];
		
		if (!Array.isArray(board)){
			// if the first one is not an array it means game is over
			gameOver(board == userName);
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
		if (chat != "") {
        var sentences = chat.split("<br />");
        if (sentences.length > 5) {
            sentences = sentences.slice(-5);
        }
        document.getElementById("textContainer").innerHTML = sentences.join("<br />") + "<br />";
		}
		
		//update the time
		document.getElementById("clock1").innerHTML = timeFirstPlayer;
		document.getElementById("clock2").innerHTML = timeSecondPlayer;
	});
}

function readyStartGame(){
	callServer("readyStartGame", "", function(response) {
		document.getElementById("startGame").remove();
    });
}

//end the game
function gameOver(winner){
	//remove the game from localStorge
	 localStorage.removeItem(userName);
	 
	if (winner)
		alert("you won");
	else
		alert("you lost");
	// Check if the element with id 'contain_game' exists
	var gameContainer = document.getElementById("contain_game");
	if (gameContainer) 
		gameContainer.remove();
	clearInterval(updateBoardInterval);
	//remove the top and the loading div if they 
	let instructions = document.getElementById('instructions');
				
	if (instructions) {
		instructions.style.display = '';
	}
	main();	
}
