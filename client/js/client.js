
	function callServer(actionToDo, valueToPass, clientNum, callback) {
		$.get("http://127.0.0.1:8000", { action: actionToDo, value: valueToPass, clientId: clientNum }, function (msg_from_server) {
			callback(msg_from_server);
		});
}
//decide which class to add to each td
function classToAdd(row,col){
		if(row == 7 && col == 1)
			return "image" + 1;
		else if (row == 7 && col < 10)
			return "image" + 2;
		else if (row == 7 ||row == 8 && col < 5)
			return "image" + 3;
		else if (row == 8 && col < 9)
			return "image" + 4;
		else if (row == 8 ||row == 9 && col < 3)
			return "image" + 5;
		else if (row == 9 && col < 7)
			return "image" + 6;	
		else if (row == 9 && col < 10)
			return "image" + 7;	
		else if (row == 9 || row == 10 && col == 1)
			return "image" + 8;
		else if (row == 10 && col == 2)
			return "image" + 9;
		else if (row == 10 && col == 3)
			return "image" + 9;
		else if (row == 10 && col < 10)
			return "bomb";
		else if (row == 10)
			return "flag";
		else if (row < 5)
			return "enemy";
		else if ([5,6].includes(row) && [3,4,7,8].includes(col))
			return "blue";
		return "green";
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