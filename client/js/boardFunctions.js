var counter = 0; // check if you need to remove the image or add it
var lastTdId; // the id of the td that we need to remove the image from
let td; // current td to add the image
	
 function createTable(rows, cols) {
    // Create a table element
    var table = document.createElement('table');

    // Create rows and cells
    for (var i = 0; i < rows; i++) {
      var row = document.createElement('tr');

      for (var j = 0; j < cols; j++) {
        var cell = document.createElement('td');
		
		cell.setAttribute('id',(i).toString() + (j).toString());
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
function moveImage(tdId,gameStarted) {
        td = document.getElementById(tdId);
		
        //if game is not started 
		if (!gameStarted){
			if (counter % 2 == 1 && tdId[0]> 5) {
				counter++;
				
				// Send the move to the server
				callServer("switchCards", lastTdId.toString() + tdId.toString(), function(response) {
					updateBoard()
				});
			
			}else if (counter % 2 == 0 && tdId[0]>5) {
				lastTdId = tdId;
				counter++;
			}
			return;
		}
		
		//if game has started
        if (counter % 2 == 1&&!td.className.includes("image")) {
            
            // Check if the location of the new image is legal
            if (!checkIfLocationOk(lastTdId, tdId))
                return;
            counter++;
            
            // Send the move to the server
            callServer("playTurn", lastTdId.toString() + tdId.toString(), function(response) {
                updateBoard()
            });
        } else if (counter % 2 == 0 &&td.className.includes("image")) {
            lastTdId = tdId;
            counter++;
        }
}

function updateBoard(){
	callServer("getBoard","", function(response) {
		if (response == "" || response === undefined)
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
