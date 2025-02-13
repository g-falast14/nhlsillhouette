document.addEventListener("DOMContentLoaded", function() {
    let guessInput = document.getElementById("player-guess");
    let submitButton = document.getElementById("submit-btn");
    let resultDisplay = document.getElementById("result");
    let nextPlayerButton = document.getElementById("next-player-btn");

    /* get user input */
    submitButton.addEventListener("click", function(){
        let userGuess = guessInput.value.trim().toLowerCase();
        let correctAnswer = guessInput.dataset.correctguess.toLowerCase();
        let resultDisplay = document.getElementById("result");

        if (userGuess == correctAnswer) {
            resultDisplay.innerHTML = "Correct!";
            resultDisplay.classList.add("text-success");
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
        loadNewPlayer();
        console.log("Successfully grabbed new player");
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let columns = document.querySelectorAll(".col");
    let headshot = document.getElementById("player-image");

    // Make headshot draggable
    headshot.addEventListener("dragstart", function(event) {
        const clonedImage = event.target.cloneNode(true);
        clonedImage.id = "cloned-headshot";
        event.dataTransfer.setData("text", event.target.id);
        event.dataTransfer.setDragImage(clonedImage, 0, 0);
    });

    // Allow columns to accept drops
    columns.forEach(column => {
        column.addEventListener("dragover", event => event.preventDefault()); // allow drop
        column.addEventListener("drop", function(event){

            event.preventDefault();
            const draggedElementId = event.dataTransfer.getData("text");
            const draggedElement = document.getElementById(draggedElementId);

            // create custom object
            const customObject = document.createElement("div");
            customObject.classList.add("custom-object");

            // clone headshot image
            const headshot = draggedElement.cloneNode(true);
            headshot.style.width = "100px";
            headshot.style.height = "100px";
            headshot.style.marginBottom = "10px";

            // player name
            const playerName = "playername";
            const label = document.createElement("p");
            label.textContent = playerName;

            // add elements to object
            customObject.appendChild(headshot);
            customObject.appendChild(label);

            let container = column.querySelector('.fwd-object-container');
            container.appendChild(customObject);

        });
    });

});