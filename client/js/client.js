
	function callServer(actionToDo, valueToPass, clientNum, callback) {
		$.get("http://127.0.0.1:8000", { action: actionToDo, value: valueToPass, clientId: clientNum }, function (msg_from_server) {
			callback(msg_from_server);
		});
}

	// Function to create the table
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

function updateBoard(){
	callServer("getBoard","",playerTurn, function(response) {
		if (response == "")
			return;
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
}

function playTurn(tdId) {

			//send the move to the other player
			callServer("isMyTurn","",playerTurn, function(response) {
				if (response == "True") {
					moveImage(tdId);
				}
				else{
					alert("waiting for opponent to play");
				}
		});
}

function classToAdd(row, col) {
	if (row < 5)
		return "green";
    if (row == 7 && col == 1){
        return "image1";
    } else if (row == 7 && col < 10) {
        return "image2";
    } else if (row == 7 || (row == 8 && col < 5)) {
        return "image3";
    } else if (row == 8 && col < 9){
        return "image4";
    } else if (row == 8 || (row == 9 && col < 3)){
        return "image5";
    } else if (row == 9 && col < 7) {
        return "image6";
    } else if (row == 9 && col < 10) {
        return "image7";
    } else if (row == 9 || (row == 10 && col == 1)) {
        return "image8";
    } else if (row == 10 && [2, 3].includes(col)) {
        return "image9";
    } else if (row == 10 && col < 10) {
        return "bomb";
    } else if (row == 10 || row == 1) {
        return "flag";
    } else if ([5, 6].includes(row) && [3, 4, 7, 8].includes(col)) {
        return "blue";
    }
    return "green";
}