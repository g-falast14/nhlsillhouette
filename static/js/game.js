document.addEventListener("DOMContentLoaded", function() {
    let guessInput = document.getElementById("player-guess");
    let submitButton = document.getElementById("submit-btn");
    let resultDisplay = document.getElementById("result");
    let nextPlayerButton = document.getElementById("next-player-btn");
    let isCorrectGuess = false; // becomes true if user guesses correctly and enables eventlisteners


    /* get user input */
    submitButton.addEventListener("click", function(){
        let userGuess = guessInput.value.trim().toLowerCase(); // get user guess
        let correctAnswer = guessInput.dataset.correctguess.toLowerCase(); // store correct answer
        let resultDisplay = document.getElementById("result"); // success/failure text

        if (userGuess == correctAnswer) {
            resultDisplay.innerHTML = "Correct!";
            resultDisplay.classList.add("text-success");
            isCorrectGuess = true;
            // make element draggable
            document.getElementById("player-image").setAttribute("draggable", "true");
        } else {
            resultDisplay.innerHTML = "Wrong! Try again.";
            resultDisplay.classList.add("text-danger");
        }
    });

    /* Function to grab new player from api and load it */
    function loadNewPlayer() {
        fetch("/get-new-player")
            .then(response => response.json())
            .then(player => {
                console.log("New player data: ", player) // debugging

                // extract new json player details
                let fullName = `${player.firstName.default} ${player.lastName.default}`;
                let newHeadshotUrl = player.headshot;

                // update image and correct guess
                let playerImage = document.getElementById("player-image");
                let guessInput = document.getElementById("player-guess");

                playerImage.src = newHeadshotUrl;
                guessInput.dataset.correctguess = fullName;

                // clear previous results and reset input field
                document.getElementById("result").innerHTML = "";
                guessInput.value = "";
            })
    }

    nextPlayerButton.addEventListener("click", function() {
        console.log("Fetching new player...");
        // reset correct guess
        isCorrectGuess = false;
        loadNewPlayer();
        console.log("Successfully grabbed new player");
    });

    // DRAG AND DROP
    // -------------------------------------------------------------------
    let columns = document.querySelectorAll(".col");
    let headshot = document.getElementById("player-image");

    // Allow columns to accept drops
    columns.forEach(column => {
        column.addEventListener("dragover", event => event.preventDefault()); // allow drop
        column.addEventListener("drop", function(event){
            event.preventDefault();

            // check if column already has a lineup object
            if (column.querySelector('.lineup-object')) {
                console.log("Column taken!");
                return;
            }

            const draggedElementId = event.dataTransfer.getData("text");
            const draggedElement = document.getElementById(draggedElementId);

            // call function to create custom object
            const lineupObject = createLineupObject(draggedElement, draggedElement.dataset.name);

            column.appendChild(lineupObject); // add object
        });
    });

    // Make headshot draggable
    headshot.addEventListener("dragstart", function(event) {
        if (isCorrectGuess) { // only allow dragging if guess is correct
            handleDragStart(event);
        } else {
            event.preventDefault(); // otherwise, prevent dragging
        }

    });

    // function to handle dragstart
    function handleDragStart(event) {
        let clonedImage = event.target.cloneNode(true); // clone image
        clonedImage.id = "cloned-headshot";
        event.dataTransfer.setData("text", event.target.id); // store original image id
        event.dataTransfer.setDragImage(clonedImage, 0, 0); // set the drag image

        console.log("Player Name", event.target.dataset.name);
    }




});

// function for creating custom lineup object
function createLineupObject(headshot, playerName) {

    const lineupObject = document.createElement("div");
    lineupObject.classList.add("lineup-object");

    // create image element
    const image = headshot.cloneNode(true);
    image.style.width = "100px";
    image.style.height = "100px";
    image.style.marginBottom = "5px";

    // create player name element
    let label = document.createElement("p");
    label.textContent = playerName;

    // append image and name to object
    lineupObject.appendChild(image);
    lineupObject.appendChild(label);

    return lineupObject;
}